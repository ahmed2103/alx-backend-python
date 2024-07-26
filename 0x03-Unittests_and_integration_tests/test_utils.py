#!/usr/bin/env python3
"""Mpdule for utils unittesting"""


import unittest
from _testclinic import TestClass
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Any, Mapping, Sequence, Dict


class TestAccessNestedMap(unittest.TestCase):
    """Class for unittesting accessing nested map function in utils module"""
    @parameterized.expand([
                            ({"a": 1}, ("a",), 1),
                            ({"a": {"b": 2}}, ("a",), {"b": 2}),
                            ({"a": {"b": 2}}, ("a", "b"), 2),
                           ])
    def test_access_nested_map(self, nested_map: Mapping,
                               path: Sequence, expected: str):
        """test_access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",),),
        ({"a": 1}, ("a", "b"),),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence):
        """tests the exception handling"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Class for unittesting getting json"""
    @parameterized.expand([
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False})
        ])
    @patch('requests.get')
    def test_get_json(self, test_url: str,
                      test_payload: Dict[str, bool], mock_get: Mock):
        """unittest for function"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Class for unittesting memoization function"""
    def test_memoize(self):
        """Function tests memoization decorator"""
        class TestClass:
            """Simple test class"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_method:
            obj = TestClass()
            res1, res2 = obj.a_property,  obj.a_property
            self.assertEqual(res1, 42)
            self.assertEqual(res2, 42)
            mock_method.assert_called_once()
