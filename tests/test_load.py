from db import load_data
import json

import pytest

def test_data_load_data_returns_list_of_dicts(tmp_path):
    json_file = tmp_path / "fake_data.json"
    fake_data = [{
    "name": "Alice Rahman",
    "email": "alice@example.com",
    "password": "password123"
  }, {
    "name": "Bob Nguyen",
    "email": "bob@example.com",
    "password": "password123"
  }]

    json_file.write_text(json.dumps(fake_data))

    result = load_data(json_file)

    assert isinstance(result, list)

def test_data_load_data_returns_correct_data(tmp_path):
    json_file = tmp_path / "fake_data.json"
    fake_data = [{
    "name": "Alice Rahman",
    "email": "alice@example.com",
    "password": "password123"
  }, {
    "name": "Bob Nguyen",
    "email": "bob@example.com",
    "password": "password123"
  }]

    json_file.write_text(json.dumps(fake_data))

    result = load_data(json_file)

    assert result[0]["email"]== "alice@example.com"


