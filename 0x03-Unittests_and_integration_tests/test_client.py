#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock
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

    def test_public_repos_url(self):
        """
        Unit-test GithubOrgClient._public_repos_url.
        Patches GithubOrgClient.org and checks that the property
        returns the expected repos_url from the mocked payload.
        """
        # Arrange
        expected_url = "https://api.github.com/orgs/test-org/repos"
        payload = {"repos_url": expected_url}

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test-org")

            # Act
            result = client._public_repos_url

            # Assert
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Unit-test GithubOrgClient.public_repos.
        Patches get_json and _public_repos_url.
        """
        # Arrange
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_payload
        expected_repos = ["repo1", "repo2", "repo3"]

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"
            client = GithubOrgClient("test-org")

            # Act
            result = client.public_repos()

            # Assert
            self.assertEqual(result, expected_repos)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")


if __name__ == "__main__":
    unittest.main()
