import os
 
os.environ.setdefault("LOG_LEVEL", "DEBUG")  
os.environ.setdefault("LOG_FILE", "test_banking.log")
 
from datetime import date, timedelta
from itertools import count
 
import pytest
 
from customer import Customer
 
 
@pytest.fixture(autouse=True)
def reset_customer_id_counter():
    """Customer.user_count is one shared counter for the whole test session,
    so without this, IDs from earlier tests would leak into later ones."""
    Customer.user_count = count(1)
    yield
 
 
@pytest.fixture
def adult_birth_date():
    today = date.today()
    return today.replace(year=today.year - 25)
 
 
@pytest.fixture
def minor_birth_date():
    today = date.today()
    return today.replace(year=today.year - 10)
 
 
@pytest.fixture(scope="session", autouse=True)
def cleanup_log_file():
    yield
    try:
        os.remove(os.environ["LOG_FILE"])
    except FileNotFoundError:
        pass
 
