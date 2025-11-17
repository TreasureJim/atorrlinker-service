import pytest
from typing import Union, List, Dict, Any
from unittest.mock import patch
import inspect

# Import the modules to test (assuming they're in the same file)
from accioaudis_sdk import Advertiser, analyze_annotation, capture_function_annotations


class TestCaptureFunctionAnnotations:
    """Test cases for capture_function_annotations function"""

    def test_capture_function_annotations_simple(self):
        """Test capturing annotations for a simple function"""

        def simple_func(x: int, y: str) -> bool:
            return True

        result = capture_function_annotations(simple_func)

        expected = {
            "name": "simple_func",
            "args": [("x", {"type_name": "int"}), ("y", {"type_name": "str"})],
            "return_type": {"type_name": "bool"},
        }
        assert result == expected

    def test_capture_function_annotations_complex(self):
        """Test capturing annotations for a function with complex types"""

        def complex_func(
            items: List[str], mapping: Dict[str, int], value: Union[str, int]
        ) -> List[Dict[str, int]]:
            return []

        result = capture_function_annotations(complex_func)

        expected = {
            "name": "complex_func",
            "args": [
                ("items", {"type_name": "List", "args": {"type_name": "str"}}),
                (
                    "mapping",
                    {
                        "type_name": "Dict",
                        "args": {"type_name": "str"},
                        "values": {"type_name": "int"},
                    },
                ),
                (
                    "value",
                    {
                        "type_name": "Union",
                        "args": [{"type_name": "str"}, {"type_name": "int"}],
                    },
                ),
            ],
            "return_type": {
                "type_name": "List",
                "args": 
                    {
                        "type_name": "Dict",
                        "args": {"type_name": "str"},
                        "values": {"type_name": "int"},
                    },
            },
        }
        assert result == expected

    def test_capture_function_annotations_no_annotations(self):
        """Test capturing annotations for a function without type annotations"""

        def unannotated_func(x, y):
            return x + y

        result = capture_function_annotations(unannotated_func)

        # inspect.signature returns inspect.Parameter.empty for missing annotations
        # which becomes {'type_name': '_empty'} in our implementation
        assert result["name"] == "unannotated_func"
        assert len(result["args"]) == 2
        assert result["return_type"]["type_name"] == "_empty"

    def test_capture_function_annotations_no_return_annotation(self):
        """Test capturing annotations for a function without return annotation"""

        def no_return_func(x: int) -> None:
            pass

        result = capture_function_annotations(no_return_func)

        expected = {
            "name": "no_return_func",
            "args": [("x", {"type_name": "int"})],
            "return_type": {"type_name": "None"},
        }
        assert result == expected
