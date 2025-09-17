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
    def test_org(self, mock_get_json, org_name):
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

    def test_public_repos_url(self):
        """
        Unit-test GithubOrgClient._public_repos_url.
        Patches GithubOrgClient.org and checks that the property
        returns the expected repos_url from the mocked payload.
        """
        # Arrange
        expected_url = "https://api.github.com/orgs/test-org/repos"
        payload = {"repos_url": expected_url}

        with patch.object(GithubOrgClient, "org", new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test-org")

            # Act
            result = client._public_repos_url

            # Assert
            self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()
