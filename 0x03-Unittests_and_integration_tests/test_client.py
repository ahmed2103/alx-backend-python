#!/usr/bin/env python3
"""Module for client unittesting"""

import unittest
from unittest.mock import patch, Mock, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Mapping
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Class to test the Github Org Client"""

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json",)
    def test_org(self, org_name: str, res: dict, mock_get_json: Mock) -> None:
        """unittesting for GithubOrgClient.org"""
        mock_get_json.return_value = res
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, res)
        mock_get_json.assert_called_once_with('https://api.github.com/orgs/{}'
                                              .format(org_name))

    def test_public_repos_url(self):
        """unittesting for GithubOrgClient.public_repos_url"""
        with patch('GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/users/google/repos"
            }
            client = GithubOrgClient('test')
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/users/google/repos")

    @patch('utils.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """unittesting for GithubOrgClient.public_repos"""
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload['repos']
        with (patch('_public_repos_url',
                    new_callable=PropertyMock) as mock_public_repos):
            mock_public_repos.return_value = test_payload['repos_url']
            self.assertEqual(GithubOrgClient("google").public_repos(),
                             ["episodes.dart", "kratu", ], )
        mock_get_json.assert_called_once()

    @parameterized.expand([({"license": {"key": "my_license"}},
                            "my_license", False),
                           ({"license": {"key": "other_license"}},
                            "my_license", False)])
    def test_has_license(self, repo: Mapping, license: str, expected: bool) -> None:
        """unittesting for GithubOrgClient.has_license"""
        self.assertIs(GithubOrgClient.has_license(repo, license), expected)

@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""
    @classmethod
    def setUpClass(cls) -> None:
        """Set up class for integration test"""
        cls.get_patcher = patch('requests.get')
        cls.get_mock = cls.get_patcher.start()

        def side_effect(url: str) -> Mock:
            """Side effected function for 'requests.get'"""
            if url.endswith('/orgs/google'):
                return Mock(json=lambda: cls.org_payload)
            elif url.endswith('/repos/google/repos'):
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: {})

        cls.get_mock.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class for integration test"""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """test public repos without filter"""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_filter(self) -> None:
        """test public repos with filter"""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos('apache-2.0'), self.apache2_repos)