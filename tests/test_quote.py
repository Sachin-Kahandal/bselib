import pytest
from bselib import bse.BSE

b = BSE()

def test_quote(script_code):
    assert len(b.quote(script_code)) == 23
