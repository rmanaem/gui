import os

import plotly.express as px
import pytest

from nerv.utility import process_files


@pytest.fixture(scope="session")
def path():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    print("Using", os.path.join(test_dir, "data"), "as the path for app")
    yield os.path.join(test_dir, "data")


@pytest.fixture(scope="session")
def data(path):
    yield process_files(path)


@pytest.fixture(scope="session")
def histogram(data):
    return px.histogram(data[data["Result"] != -1], x="Result", template="plotly_dark")
