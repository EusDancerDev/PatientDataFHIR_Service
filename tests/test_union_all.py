#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test module for UNION ALL implementation.

This module contains tests for the filter_data_consolidated function,
which implements a UNION ALL approach for querying multiple tables.
"""

# Import modules #
#----------------#

from datetime import datetime
import unittest
from sqlalchemy import Column, Integer, String, DateTime
from unittest.mock import MagicMock, patch

# Import project modules #
#------------------------#

from app.db import filter_data_consolidated, BaseModel

# Define test models #
#--------------------#

class TestModelA(BaseModel):
    """Test model A for UNION ALL testing."""
    __tablename__ = 'test_table_a'
    
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

class TestModelB(BaseModel):
    """Test model B for UNION ALL testing."""
    __tablename__ = 'test_table_b'
    
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

# Define test cases #
#-------------------#

class TestUnionAll(unittest.TestCase):
    """Test cases for UNION ALL implementation."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a mock session
        self.session = MagicMock()
        
        # Create model registry
        self.model_registry = {
            'test_table_a': TestModelA,
            'test_table_b': TestModelB
        }
        
        # Sample request data
        self.request_data = {
            'id_patient': '0000021561',
            'date_range': {
                'min_date': '2023-01-01',
                'max_date': '2023-01-31'
            }
        }
        
        # Mock the session.execute method to return some results
        self.mock_result_proxy = MagicMock()
        self.session.execute.return_value = self.mock_result_proxy
        
        # Mock row objects to be returned by the result proxy
        row_a = MagicMock()
        row_a.source_table = 'test_table_a'
        row_a.data = {
            'id': 1,
            'id_patient': '0000021561',
            'value': 42,
            'recorded_at': datetime(2023, 1, 15, 12, 0, 0)
        }
        
        row_b = MagicMock()
        row_b.source_table = 'test_table_b'
        row_b.data = {
            'id': 1,
            'id_paciente': '0000021561',
            'measurement': 120,
            'fecha_registro': datetime(2023, 1, 15, 14, 0, 0)
        }
        
        self.mock_result_proxy.__iter__.return_value = [row_a, row_b]
    
    @patch('app.db.parse_dt_string')
    @patch('app.db.union_all')
    @patch('app.db.select')
    def test_filter_data_consolidated(self, mock_select, mock_union_all, mock_parse_dt_string):
        """Test the filter_data_consolidated function."""
        # Configure parse_dt_string mock to return valid datetime objects
        mock_parse_dt_string.side_effect = [
            datetime(2023, 1, 1, 0, 0, 0),  # min_date
            datetime(2023, 1, 31, 23, 59, 0)  # max_date
        ]
        
        # Configure select mock
        mock_select.return_value.select_from.return_value.where.return_value.where.return_value.where.return_value = "SELECT QUERY"
        
        # Configure union_all mock
        mock_union_all.return_value = "UNION ALL QUERY"
        
        # Call the function being tested
        results = filter_data_consolidated(
            self.session,
            self.request_data,
            ['test_table_a', 'test_table_b'],
            self.model_registry
        )
        
        # Assert union_all was called
        mock_union_all.assert_called_once()
        
        # Assert session.execute was called with the UNION ALL query
        self.session.execute.assert_called_once_with("UNION ALL QUERY")
        
        # Check results were properly organized by table
        self.assertIn('test_table_a', results)
        self.assertIn('test_table_b', results)
        
        # Check instance types
        self.assertIsInstance(results['test_table_a'][0], TestModelA)
        self.assertIsInstance(results['test_table_b'][0], TestModelB)
        
        # Check values were correctly transferred
        self.assertEqual(results['test_table_a'][0].value, 42)
        self.assertEqual(results['test_table_b'][0].measurement, 120)

# Main execution #
#----------------#

if __name__ == '__main__':
    unittest.main() 