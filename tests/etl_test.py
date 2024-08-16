import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from datetime import date
from etl.etl import Etl
import pytest
import pandas as pd


@pytest.fixture
def etl():
    # Use a mock logger factory
    return Etl(log_file='mock_log.log')


def test_classify_size(etl):
    assert etl._classify_size(5) == 'Micro'
    assert etl._classify_size(25) == 'Small'
    assert etl._classify_size(100) == 'Medium'
    assert etl._classify_size(500) == 'Large'
    assert etl._classify_size(1500) == 'Very Large'


def test_classify_age(etl):
    current_year = date.today().year
    assert etl._classify_age(current_year - 5) == 'Emerging'
    assert etl._classify_age(current_year - 30) == 'Established'
    assert etl._classify_age(current_year - 50) == 'Legacy'


def check_col_names(df):
    # Check for uppercase letters in column names
    uppercase_columns = [col for col in df.columns if any(char.isupper() for char in col)]
    assert not uppercase_columns, f"Columns contain uppercase letters: {uppercase_columns}"

    # Check for spaces in column names
    space_columns = [col for col in df.columns if ' ' in col]
    assert not space_columns, f"Columns contain spaces: {space_columns}"


def test_apply_transformations(etl):
    # Create a DataFrame with test data
    test_data = {
        'founded': ['2000', '1980', '1965', '2024'],
        'number_of_employees': [300, 30, 1200, 5]
    }
    df = pd.DataFrame(test_data)

    # Apply transformations
    result_df = etl._apply_transformations(df)
    check_col_names(result_df)

    # Check transformed columns
    assert 'maturity_level' in result_df.columns
    assert 'organization_size' in result_df.columns

    # Validate the transformation logic
    assert result_df['maturity_level'].iloc[0] == 'Established'
    assert result_df['organization_size'].iloc[0] == 'Large'
    assert result_df['maturity_level'].iloc[1] == 'Legacy'
    assert result_df['organization_size'].iloc[1] == 'Small'
    assert result_df['maturity_level'].iloc[2] == 'Legacy'
    assert result_df['organization_size'].iloc[2] == 'Very Large'
    assert result_df['maturity_level'].iloc[3] == 'Emerging'
    assert result_df['organization_size'].iloc[3] == 'Micro'
