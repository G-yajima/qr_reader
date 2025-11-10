import pandas as pd

from src.format_excel import format_excel

import pytest

def test_data_format_missing_columns():
    data = pd.read_excel("tests/data/TestExcel_test2_no_include_colmun.xlsx")
    required_cols = ["Label", "Location", "User"]

    with pytest.raises(ValueError, match="次の列が見つかりません"):
        format_excel(data, required_cols)

