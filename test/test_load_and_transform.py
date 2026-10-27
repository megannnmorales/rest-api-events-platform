from db.load_and_transform import load_data
from db.load_and_transform import get_city
from db.load_and_transform import get_postcode
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


def test_no_address_returns_no_city():
    venue = {
      "name": "Online – Zoom",
      "address": None,
      "capacity": 500
    }
    
    expected = None
    result = get_city(venue)
    
    assert result == expected

def test_address_returns_city():
  venue = {
    "name": "Nexus, University of Leeds",
    "address": "Discovery Way, Leeds, LS2 3AA",
    "capacity": 200
  }

  expected = "Leeds"
  result = get_city(venue)

  assert result == expected

def test_no_address_returns_no_postcode():
    venue = {
          "name": "Online – Zoom",
          "address": None,
          "capacity": 500
        }
        
    expected = None
    result = get_postcode(venue)
        
    assert result == expected

def test_address_returns_postcode():
    venue = {
        "name": "Nexus, University of Leeds",
        "address": "Discovery Way, Leeds, LS2 3AA",
        "capacity": 200
      }

    expected = "LS2 3AA"
    result = get_postcode(venue)

    assert result == expected