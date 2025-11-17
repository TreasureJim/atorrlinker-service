import pytest
from typing import Union, List, Dict, Any
from unittest.mock import patch
import inspect

# Import the modules to test (assuming they're in the same file)
from accioaudis_sdk import Advertiser, analyze_annotation, capture_function_annotations


class TestAnalyzeAnnotation:
    """Test cases for analyze_annotation function"""

    def test_analyze_annotation_primitive_types(self):
        """Test analyzing primitive type annotations"""
        assert analyze_annotation(str) == {"type_name": "str"}
        assert analyze_annotation(int) == {"type_name": "int"}
        assert analyze_annotation(float) == {"type_name": "float"}
        assert analyze_annotation(bool) == {"type_name": "bool"}

    def test_analyze_annotation_union(self):
        """Test analyzing Union type annotations"""
        result = analyze_annotation(Union[str, int])
        expected = {
            "type_name": "Union",
            "args": [{"type_name": "str"}, {"type_name": "int"}],
        }
        assert result == expected

    def test_analyze_annotation_list(self):
        """Test analyzing List type annotations"""
        result = analyze_annotation(List[str])
        expected = {"type_name": "List", "args": {"type_name": "str"}}
        assert result == expected

        # Test nested list
        result = analyze_annotation(List[List[int]])
        expected = {
            "type_name": "List",
            "args": {"type_name": "List", "args": {"type_name": "int"}},
        }
        assert result == expected

    def test_analyze_annotation_dict(self):
        """Test analyzing Dict type annotations"""
        result = analyze_annotation(Dict[str, int])
        expected = {
            "type_name": "Dict",
            "args": {"type_name": "str"},
            "values": {"type_name": "int"},
        }
        assert result == expected

        # Test complex dict
        result = analyze_annotation(Dict[str, List[int]])
        expected = {
            "type_name": "Dict",
            "args": {"type_name": "str"},
            "values": {"type_name": "List", "args": {"type_name": "int"}},
        }
        assert result == expected

    def test_analyze_annotation_complex_union(self):
        """Test analyzing complex Union types"""
        result = analyze_annotation(Union[List[str], Dict[str, int]])
        expected = {
            "type_name": "Union",
            "args": [
                {"type_name": "List", "args": {"type_name": "str"}},
                {
                    "type_name": "Dict",
                    "args": {"type_name": "str"},
                    "values": {"type_name": "int"},
                },
            ],
        }
        assert result == expected

    def test_analyze_annotation_any(self):
        """Test analyzing Any type"""
        result = analyze_annotation(Any)
        assert result == {"type_name": "Any"}
