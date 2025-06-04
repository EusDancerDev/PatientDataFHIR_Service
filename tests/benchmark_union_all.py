#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Benchmark module for UNION ALL implementation.

This module contains benchmark tests comparing the performance of:
1. Individual queries for each table
2. UNION ALL approach for consolidated queries

The benchmark measures execution time and result consistency between both approaches.
"""

# Import modules #
#----------------#

import argparse
import random
import time
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text

# Import project modules #
#------------------------#
from app.config import DATABASE_CREDENTIALS
from app.db import BaseModel, filter_data_consolidated

# Define test models #
#--------------------#

Base = declarative_base()

class TestTableA(BaseModel):
    """Test table A for benchmarking."""
    __tablename__ = 'benchmark_table_a'
    
    id = Column(Integer, primary_key=True)
    id_patient = Column(String(10))
    value = Column(Integer)
    recorded_at = Column(DateTime)
    
    @classmethod
    def get_patient_id_field(cls):
        return cls.id_patient
        
    @classmethod
    def get_date_field(cls):
        return cls.recorded_at
    
    def to_hl7_v2(self):
        return f"MSH|^~\\&|BENCHMARK|BENCHMARK||TABLE_A||{self.recorded_at}||OBX|1|NM|VALUE|{self.value}|"

class TestTableB(BaseModel):
    """Test table B for benchmarking."""
    __tablename__ = 'benchmark_table_b'
    
    id = Column(Integer, primary_key=True)
    id_paciente = Column(String(10))
    measurement = Column(Integer)
    fecha_registro = Column(DateTime)
    
    @classmethod
    def get_patient_id_field(cls):
        return cls.id_paciente
        
    @classmethod
    def get_date_field(cls):
        return cls.fecha_registro
    
    def to_hl7_v2(self):
        return f"MSH|^~\\&|BENCHMARK|BENCHMARK||TABLE_B||{self.fecha_registro}||OBX|1|NM|MEASUREMENT|{self.measurement}|"

class TestTableC(BaseModel):
    """Test table C for benchmarking."""
    __tablename__ = 'benchmark_table_c'
    
    id = Column(Integer, primary_key=True)
    id_paciente_temp = Column(String(10))
    temperature = Column(Integer)
    fecha_registro_temp = Column(DateTime)
    
    @classmethod
    def get_patient_id_field(cls):
        return cls.id_paciente_temp
        
    @classmethod
    def get_date_field(cls):
        return cls.fecha_registro_temp
    
    def to_hl7_v2(self):
        return f"MSH|^~\\&|BENCHMARK|BENCHMARK||TABLE_C||{self.fecha_registro_temp}||OBX|1|NM|TEMPERATURE|{self.temperature}|"

# Define helper functions #
#-------------------------#

def setup_database():
    """Set up database connection and create test tables."""
    print("Setting up database connection...")
    engine = create_engine(
        f"postgresql://{DATABASE_CREDENTIALS['username']}:{DATABASE_CREDENTIALS['password']}@"
        f"{DATABASE_CREDENTIALS['host']}:{DATABASE_CREDENTIALS['port']}/{DATABASE_CREDENTIALS['database_name']}"
    )
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()
    
    return engine, session

def populate_test_data(session, patient_count, records_per_patient):
    """Populate test tables with sample data."""
    print(f"Populating test data: {patient_count} patients with {records_per_patient} records each...")
    
    # Generate patient IDs
    patient_ids = [f"{i:010d}" for i in range(1, patient_count + 1)]
    
    # Base date for records
    base_date = datetime(2023, 1, 1)
    
    # Clear existing data
    for table in [TestTableA, TestTableB, TestTableC]:
        session.query(table).delete()
    
    # Insert data for each patient
    for patient_id in patient_ids:
        for i in range(records_per_patient):
            # Create a record for each table with a slightly different timestamp
            record_date = base_date + timedelta(hours=i)
            
            # Table A record
            session.add(TestTableA(
                id_patient=patient_id,
                value=random.randint(50, 150),
                recorded_at=record_date
            ))
            
            # Table B record
            session.add(TestTableB(
                id_paciente=patient_id,
                measurement=random.randint(80, 200),
                fecha_registro=record_date + timedelta(minutes=10)
            ))
            
            # Table C record
            session.add(TestTableC(
                id_paciente_temp=patient_id,
                temperature=random.randint(350, 390),  # in tenths of a degree
                fecha_registro_temp=record_date + timedelta(minutes=20)
            ))
    
    # Commit the changes
    session.commit()
    print(f"Test data population complete. Added {patient_count * records_per_patient * 3} records.")

def run_original_implementation(session, request_data, table_names, model_registry):
    """Run the original implementation that uses separate queries."""
    results = {}
    
    # Extract common filter values
    patient_id = request_data['id_patient']
    date_data = request_data['date_range']
    min_value = date_data['min_date']
    max_value = date_data['max_date']
    
    # For each table, run a separate query
    for table_name in table_names:
        if table_name not in model_registry:
            continue
            
        model_class = model_registry[table_name]
        
        # Get field mappings for this table
        id_field = model_class.get_patient_id_field()
        date_field = model_class.get_date_field()
        
        if id_field is None or date_field is None:
            continue
            
        # Build query for this table
        query = session.query(model_class).filter(id_field == patient_id)
        
        # Apply date range filter
        from app.db import _apply_date_range_filter
        query = _apply_date_range_filter(query, min_value, max_value, date_field)
        
        # Execute and store results
        table_results = query.all()
        if table_results:
            results[table_name] = table_results
    
    return results

def benchmark(session, iterations=10):
    """Run benchmark comparing the two implementations."""
    print(f"Running benchmark with {iterations} iterations...")
    
    # Set up model registry
    model_registry = {
        'benchmark_table_a': TestTableA,
        'benchmark_table_b': TestTableB,
        'benchmark_table_c': TestTableC
    }
    
    # Table names to query
    table_names = list(model_registry.keys())
    
    # Prepare request data - use patient ID 1
    request_data = {
        'id_patient': '0000000001',
        'date_range': {
            'min_date': '2023-01-01',
            'max_date': '2023-01-31'
        }
    }
    
    # Results storage
    original_times = []
    union_all_times = []
    
    # Run benchmark iterations
    for i in range(iterations):
        print(f"Iteration {i+1}/{iterations}")
        
        # Benchmark original implementation
        start_time = time.time()
        original_results = run_original_implementation(
            session, request_data, table_names, model_registry
        )
        end_time = time.time()
        original_duration = end_time - start_time
        original_times.append(original_duration)
        print(f"  Original implementation: {original_duration:.6f} seconds - {sum(len(results) for results in original_results.values())} records")
        
        # Benchmark UNION ALL implementation
        start_time = time.time()
        union_all_results = filter_data_consolidated(
            session, request_data, table_names, model_registry
        )
        end_time = time.time()
        union_all_duration = end_time - start_time
        union_all_times.append(union_all_duration)
        print(f"  UNION ALL implementation: {union_all_duration:.6f} seconds - {sum(len(results) for results in union_all_results.values())} records")
        
        # Verify result counts match
        original_count = sum(len(results) for results in original_results.values())
        union_all_count = sum(len(results) for results in union_all_results.values())
        if original_count != union_all_count:
            print(f"  WARNING: Result counts differ! Original: {original_count}, UNION ALL: {union_all_count}")
    
    # Calculate and display summary statistics
    avg_original = sum(original_times) / len(original_times)
    avg_union_all = sum(union_all_times) / len(union_all_times)
    
    improvement_pct = (1 - (avg_union_all / avg_original)) * 100
    
    print("\nBenchmark Results:")
    print(f"Original Implementation (average): {avg_original:.6f} seconds")
    print(f"UNION ALL Implementation (average): {avg_union_all:.6f} seconds")
    print(f"Improvement: {improvement_pct:.2f}%")

# Main execution #
#----------------#

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Benchmark UNION ALL vs separate queries')
    parser.add_argument('--patients', type=int, default=100, help='Number of patients to test with')
    parser.add_argument('--records', type=int, default=10, help='Records per patient')
    parser.add_argument('--iterations', type=int, default=10, help='Number of benchmark iterations')
    args = parser.parse_args()
    
    # Set up database
    engine, session = setup_database()
    
    try:
        # Populate test data
        populate_test_data(session, args.patients, args.records)
        
        # Run benchmark
        benchmark(session, args.iterations)
        
    finally:
        # Clean up
        session.close()
        engine.dispose()

if __name__ == '__main__':
    main() 