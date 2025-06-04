#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from sqlalchemy import create_engine, text, select, union_all
from sqlalchemy.sql.expression import cast, literal_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus
from typing import Dict

#------------------------#
# Import project modules #
#------------------------#

from app.utils.time_formatters import parse_dt_string
from app.constants.error_messages import (
    INVALID_DATE_FORMAT_ERROR,
    INVALID_DATE_RANGE_ERROR
)

#-----------------#
# Declare objects #
#-----------------#

# SQLAlchemy Base class #
Base = declarative_base()

# Model registry to store all models
MODEL_REGISTRY = {}

#------------------#
# Define functions #
#------------------#

# %% Helpers

# Database connections #
#----------------------#

def _init_engine(config, database_type):
    """
    Create a SQLAlchemy engine based on provided credentials and database type.

    Parameters
    ----------
    config : dict
        Contains credentials for accessing the database with keys:
        - 'username': str, the database username.
        - 'password': str, the database password.
        - 'host': str, the database host address.
        - 'port': str, optional, the database port.
        - 'database_name': str, optional, the name of the database.

    database_type : {'mysql', 'postgresql', 'sqlite'}
        The type of database for SQLAlchemy configuration.

    Returns
    -------
    sqlalchemy.engine.base.Engine
        A configured SQLAlchemy engine object for database interactions.

    Note
    ----
    Use URL-encoded passwords with special characters (e.g., '@') using `urllib.parse.quote_plus`.
    """
    if database_type.lower() == "postgresql":
        # PostgreSQL connection string
        connection_string = (
            f"postgresql://{config['username']}:{quote_plus(config['password'])}@"
            f"{config['host']}:{config['port']}/{config['database_name']}"
        )
        engine = create_engine(connection_string)
        return engine
    else:
        raise ValueError(f"Unsupported database type: {database_type}")

def init_db(config, database_type="postgresql"):
    """
    Initialise the database connection and create tables.
    """
    engine = _init_engine(config, database_type)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session

def _apply_date_range_filter(query, min_value, max_value, date_field):
    """
    Apply date range filter, always including both edges of the range.

    Parameters
    ----------
    query : sqlalchemy.orm.query.Query
        The current query object.
    min_value : str
        Start date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'.
        If only date is provided, time defaults to 00:00.
    max_value : str
        End date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'.
        If only date is provided, time defaults to 23:59.
    date_field : sqlalchemy.Column
        The date field to filter on.

    Returns
    -------
    sqlalchemy.orm.query.Query
        Query with date range filter applied.

    Raises
    ------
    ValueError
        If date format is incorrect.
    """
    try:
        # Try parsing with time first
        try:
            min_date = parse_dt_string(min_value, '%Y-%m-%d %H:%M')
        except ValueError:
            # If that fails, try date-only format and set time to 00:00
            min_date = parse_dt_string(min_value, '%Y-%m-%d')
            min_date = min_date.replace(hour=0, minute=0)

        try:
            max_date = parse_dt_string(max_value, '%Y-%m-%d %H:%M')
        except ValueError:
            # If that fails, try date-only format and set time to 23:59
            max_date = parse_dt_string(max_value, '%Y-%m-%d')
            max_date = max_date.replace(hour=23, minute=59)

    except ValueError:
        raise ValueError(INVALID_DATE_FORMAT_ERROR)

    if min_date > max_date:
        raise ValueError(INVALID_DATE_RANGE_ERROR)

    # Always include both edges of the range
    query = query.filter(date_field >= min_date, date_field <= max_date)
    return query

def filter_data(session_or_factory, request_data, model_class=None):
    """
    Filter data based on request parameters for a single table.
    
    This is a wrapper around filter_data_consolidated for backward compatibility.
    It handles the case of a single table/model class.
    
    Parameters
    ----------
    session_or_factory: Session or SessionFactory
        SQLAlchemy session or session factory
    request_data: Dict
        Dictionary with query parameters
    model_class: Type[BaseModel]
        SQLAlchemy model class to query
        
    Returns
    -------
    List[BaseModel]
        List of model instances matching the query
    """
    try:
        if model_class is None:
            raise ValueError("Model class is required for filtering")
            
        # Find the table name for this model class
        table_name = model_class.__tablename__
        
        # Create a temporary registry with just this model
        temp_registry = {table_name: model_class}
        
        # Use the consolidated function with a single table
        results = filter_data_consolidated(
            session_or_factory,
            request_data,
            [table_name],
            temp_registry
        )
        
        # Return the results for this table, or empty list if none found
        return results.get(table_name, [])
        
    except Exception as e:
        # Maintain the same error handling as before
        if callable(session_or_factory):
            session = session_or_factory()
            session.rollback()
            session.close()
        raise e

def filter_data_consolidated(session_or_factory, request_data, table_names, model_registry):
    """
    Filter data from multiple tables in a single consolidated query using UNION ALL.
    
    This implementation uses a true UNION ALL SQL query which provides several advantages:
    1. Sends only a single query to the database server, reducing network latency
    2. The database engine can optimise the overall execution plan
    3. Improves performance by eliminating multiple individual queries
    4. Reduces connection overhead when working with multiple tables
    
    Parameters
    ----------
    session_or_factory: Session or SessionFactory
        SQLAlchemy session or session factory
    request_data: Dict
        Dictionary with query parameters (id_patient, date_range)
    table_names: List[str]
        List of table names to query
    model_registry: Dict
        Dictionary mapping table names to model classes
        
    Returns
    -------
    Dict
        Dictionary mapping table names to query results
    """
    try:
        # Create session if factory is provided
        if callable(session_or_factory):
            session = session_or_factory()
        else:
            session = session_or_factory
            
        # Extract common filter values
        if 'id_patient' not in request_data:
            raise ValueError("Missing required ID field in request data")
            
        if 'date_range' not in request_data:
            raise ValueError("Missing required date range in request data")
            
        patient_id = request_data['id_patient']
        date_data = request_data['date_range']
        
        if not isinstance(date_data, dict) or 'min_date' not in date_data or 'max_date' not in date_data:
            raise ValueError("invalid date range format in request data")
            
        min_value = date_data['min_date']
        max_value = date_data['max_date']
        
        # Parse dates for all tables
        try:
            # Try parsing with time first
            try:
                min_date = parse_dt_string(min_value, '%Y-%m-%d %H:%M')
            except ValueError:
                # If that fails, try date-only format and set time to 00:00
                min_date = parse_dt_string(min_value, '%Y-%m-%d')
                min_date = min_date.replace(hour=0, minute=0)

            try:
                max_date = parse_dt_string(max_value, '%Y-%m-%d %H:%M')
            except ValueError:
                # If that fails, try date-only format and set time to 23:59
                max_date = parse_dt_string(max_value, '%Y-%m-%d')
                max_date = max_date.replace(hour=23, minute=59)

        except ValueError:
            raise ValueError(INVALID_DATE_FORMAT_ERROR)

        if min_date > max_date:
            raise ValueError(INVALID_DATE_RANGE_ERROR)
            
        # Build individual selects for the UNION ALL
        union_queries = []
        
        for table_name in table_names:
            if table_name not in model_registry:
                continue
                
            model_class = model_registry[table_name]
            
            # Get field mappings for this table
            id_field = model_class.get_patient_id_field()
            date_field = model_class.get_date_field()
            
            if id_field is None or date_field is None:
                continue
            
            # Get the actual table for reflection
            table = model_class.__table__
            
            # Select statement with all columns from this table and a source table name column
            query = (
                select(
                    literal_column(f"'{table_name}'").label('source_table'),
                    # Convert all columns to a JSON object
                    cast(text(f"row_to_json({table.name}.*)"), JSONB).label('data')
                )
                .select_from(table)
                .where(id_field == patient_id)
                .where(date_field >= min_date)
                .where(date_field <= max_date)
            )
            
            union_queries.append(query)
        
        # Combine all queries with UNION ALL
        if not union_queries:
            return {}
            
        final_query = union_all(*union_queries)
        
        # Execute the union all query
        result_proxy = session.execute(final_query)
        
        # Process the results back into the expected format
        results = {}
        for row in result_proxy:
            source_table = row.source_table
            data = row.data
            
            # Initialize list for this table if it doesn't exist
            if source_table not in results:
                results[source_table] = []
                
            # Instantiate the model class with the data
            model_class = model_registry[source_table]
            model_instance = model_class()
            
            # Apply data to model instance
            for key, value in data.items():
                if hasattr(model_instance, key):
                    setattr(model_instance, key, value)
                    
            # Add the model instance to the results
            results[source_table].append(model_instance)
            
        return results
        
    except Exception as e:
        # Clean up session if it was created here
        if callable(session_or_factory):
            session.rollback()
            session.close()
        raise e

# %% Main methods

# Base model definition #
#-----------------------#

class BaseModel(Base):
    """
    Base model class with common fields and methods for all models.
    
    This class serves as a base for all other model classes in the application.
    It provides common fields and methods that are shared across all models.
    """
    __abstract__ = True
    
    def to_hl7_v2(self) -> str:
        """
        Convert the model instance to an HL7 v2.x message.
        
        This method should be overridden by child classes to provide
        specific HL7 message formatting based on their data structure.
        
        Returns
        -------
        str
            The HL7 v2.x formatted message string
        """
        raise NotImplementedError("Subclasses must implement to_hl7_v2()")
    
    def to_fhir_v5(self) -> Dict:
        """
        Convert the model instance to a FHIR v5 resource.
        
        This method should be overridden by child classes to provide
        specific FHIR resource formatting based on their data structure.
        
        Returns
        -------
        Dict
            The FHIR v5 resource as a dictionary
        """
        raise NotImplementedError("Subclasses must implement to_fhir_v5()")
    
    @classmethod
    def get_patient_id_field(cls):
        """
        Get the patient ID field for this model.
        
        Returns
        -------
        sqlalchemy.Column
            The patient ID column for this model.
        """
        from app.constants.table_mappings import TABLE_FIELD_MAPPING
        if cls.__tablename__ in TABLE_FIELD_MAPPING:
            field_name = TABLE_FIELD_MAPPING[cls.__tablename__]['id_field']
            if field_name:
                return getattr(cls, field_name)
        return None
    
    @classmethod
    def get_date_field(cls):
        """
        Get the date field for this model.
        
        Returns
        -------
        sqlalchemy.Column
            The date column for this model.
        """
        from app.constants.table_mappings import TABLE_FIELD_MAPPING
        if cls.__tablename__ in TABLE_FIELD_MAPPING:
            field_name = TABLE_FIELD_MAPPING[cls.__tablename__]['date_field']
            if field_name:
                return getattr(cls, field_name)
        return None

    @classmethod
    def register_model(cls, table_name: str):
        """
        Register the model in the MODEL_REGISTRY.
        
        Parameters
        ----------
        table_name : str
            The name of the table this model represents.
        """
        MODEL_REGISTRY[table_name] = cls
        return cls  # Return the class to allow for decorator-style usage if needed

#--------------------------#

# Switch dictionaries #
#---------------------#

# Database aliases #
db_alias_dict = {
    "mysql" : "mysql+pymysql",
    "postgresql" : "postgresql",
    "sqlite" : "sqlite"
}

# %%
