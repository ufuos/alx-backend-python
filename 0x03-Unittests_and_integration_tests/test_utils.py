#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map and utils.get_json.

These tests verify behavior for nested-map access and for fetching JSON
from an HTTP endpoint while mocking external requests.
"""

import unittest
from typing import Any, Dict, Tuple
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict[str, Any], path: Tuple[str, ...], expected: Any) -> None:
        """Test that access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),                  # empty dict, missing key
        ({"a": 1}, ("a", "b")),        # value is not a dict, so "b" fails
    ])
    def test_access_nested_map_exception(self, nested_map: Dict[str, Any], path: Tuple[str, ...]) -> None:
        """Test that KeyError is raised for invalid paths with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Check that the exception message matches the missing key
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json using mocked HTTP calls."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url: str, test_payload: Dict[str, Any], mock_get: Mock) -> None:
        """Test that get_json returns expected result with mocked requests."""
        # Configure mock to return a response with .json() method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call function under test
        result = get_json(test_url)

        # Assert requests.get was called once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert result matches expected payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
