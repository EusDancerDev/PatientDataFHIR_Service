# UNION ALL Implementation Documentation

## Overview

This document details the implementation of a true SQL UNION ALL query in the PatientDataFHIR_Service system to optimize data retrieval across multiple tables. This enhancement replaces the previous approach of making separate queries for each table, resulting in improved performance and reduced database load.

## Implementation Details

### Core Changes

1. **Modified `filter_data_consolidated` Function**
   - Rewrote the function in `app/db.py` to use SQLAlchemy's `union_all` operation
   - Replaced multiple individual queries with a single UNION ALL query
   - Added table source tracking to properly reconstruct model instances from query results

2. **Added SQLAlchemy Imports**
   - Added necessary SQLAlchemy imports to support UNION ALL operations:
     ```python
     from sqlalchemy import text, select, union_all
     from sqlalchemy.sql.expression import cast, literal_column
     from sqlalchemy.dialects.postgresql import JSONB
     ```

3. **Row Data Conversion**
   - Implemented a mechanism to convert JSON row data back into model instances
   - Added source table tracking to ensure results are organized correctly

### Technical Implementation

The UNION ALL query works by:

1. Building individual SELECT statements for each table with:
   - A literal column for the source table name 
   - A JSON representation of the entire row's data
   - Appropriate WHERE clauses for patient ID and date range filtering

2. Combining the individual queries with `union_all`

3. Executing a single database query

4. Reconstructing model instances from the JSON data based on source table

Example query structure:
```sql
SELECT 'table1' AS source_table, row_to_json(table1.*) AS data
FROM table1
WHERE id_patient = '0000021561' AND recorded_at BETWEEN '2023-01-01' AND '2023-01-31'

UNION ALL

SELECT 'table2' AS source_table, row_to_json(table2.*) AS data
FROM table2
WHERE id_paciente = '0000021561' AND fecha_registro BETWEEN '2023-01-01' AND '2023-01-31'
```

## Performance Benefits

The UNION ALL approach provides several key benefits:

1. **Reduced Database Round-trips**
   - Only a single query is executed instead of multiple queries
   - Minimizes network latency between application and database

2. **Optimized Execution Plan**
   - Allows the database to optimize the execution of the entire query
   - Potentially improves cache utilization and query planning

3. **Simplified Connection Management**
   - Reduces the number of active database connections needed
   - Eliminates potential threading issues when querying multiple tables

4. **Improved Scalability**
   - Performance benefits increase with more tables or more complex queries
   - Better handles large result sets

## Testing

A comprehensive testing approach was implemented:

1. **Unit Tests**
   - Created `tests/test_union_all.py` to test the UNION ALL functionality
   - Mocked database interactions to ensure correct behavior

2. **Benchmarking**
   - Implemented `benchmark_union_all.py` script to compare performance
   - Measures execution time for both the original and UNION ALL implementations
   - Supports configurable test parameters (patients, records, iterations)

## Usage Example

The UNION ALL implementation is used automatically when calling:

```python
from app.services.vital_signs_service import VitalSignsService

vital_signs_service = VitalSignsService(patient_service)
results = vital_signs_service.retrieve_all_vital_signs(
    patient_id='0000021561',
    start_date='2023-01-01',
    end_date='2023-01-31'
)
```

## Backward Compatibility

This implementation maintains backward compatibility with existing code:

- The `filter_data` function continues to work as before, now calling `filter_data_consolidated`
- The API interface remains unchanged, with performance improvements happening transparently
- All existing unit tests should continue to pass

## Future Improvements

Potential areas for further optimization include:

1. Implementing type-specific UNION ALL queries for specific data types
2. Adding query result caching for frequently accessed data
3. Supporting more complex filtering criteria in the UNION ALL queries
4. Adding pagination support for large result sets 