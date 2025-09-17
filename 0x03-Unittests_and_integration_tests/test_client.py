#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the expected value
        and get_json is called once with the correct URL.
        """
        # Arrange
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"org": org_name}
        client = GithubOrgClient(org_name)

        # Act
        result = client.org

        # Assert
        self.assertEqual(result, {"org": org_name})
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
