#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map, utils.get_json, and utils.memoize.
"""

import unittest
from typing import Any, Dict, Tuple
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str, ...],
        expected: Any
    ) -> None:
        """Test that access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),            # empty dict, missing key
        ({"a": 1}, ("a", "b")),  # value is not a dict, so "b" fails
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str, ...]
    ) -> None:
        """
        Test that KeyError is raised for invalid paths
        and that the exception message matches the missing key.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # KeyError message includes repr of the key, e.g. "'a'"
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json using mocked HTTP calls."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict[str, Any],
        mock_get: Mock
    ) -> None:
        """Test that get_json returns expected result with mocked requests."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches method results."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=42
        ) as mock_method:
            obj = TestClass()

            result1 = obj.a_property()
            self.assertEqual(result1, 42)

            result2 = obj.a_property()
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
