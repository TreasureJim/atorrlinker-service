import pytest
from typing import Union, List, Dict, Any
from unittest.mock import patch
import inspect

# Import the modules to test (assuming they're in the same file)
from accioaudis_sdk import Advertiser, analyze_annotation, capture_function_annotations


class TestAdvertiser:
    """Test cases for Advertiser class"""

    def test_advertiser_initialization(self):
        """Test that Advertiser initializes with empty functions dict"""
        advertiser = Advertiser()
        assert advertiser.functions == {}

    def test_search_decorator_registers_function(self):
        """Test that @search decorator properly registers functions"""
        advertiser = Advertiser()

        @advertiser.search()
        def test_function(x: int, y: str) -> bool:
            return True

        # Check that function is registered
        assert "test_function" in advertiser.functions
        assert advertiser.functions["test_function"]["function"] is test_function

        # Check that annotations are captured
        annotations = advertiser.functions["test_function"]["args"]
        assert annotations["name"] == "test_function"
        assert len(annotations["args"]) == 2

    def test_search_decorator_preserves_function_behavior(self):
        """Test that decorated function still works normally"""
        advertiser = Advertiser()

        @advertiser.search()
        def add_numbers(a: int, b: int) -> int:
            return a + b

        # Test that function still works
        result = add_numbers(5, 3)
        assert result == 8

    def test_multiple_functions_registration(self):
        """Test that multiple functions can be registered"""
        advertiser = Advertiser()

        @advertiser.search()
        def func1(x: int) -> str:
            return str(x)

        @advertiser.search()
        def func2(y: str) -> List[int]:
            return [1, 2, 3]

        assert "func1" in advertiser.functions
        assert "func2" in advertiser.functions
        assert len(advertiser.functions) == 2

    def test_function_with_complex_types_registration(self):
        """Test registration of function with complex type annotations"""
        advertiser = Advertiser()

        @advertiser.search()
        def process_data(
            items: List[Dict[str, Union[int, float]]], config: Dict[str, Any]
        ) -> List[str]:
            return ["result"]

        assert "process_data" in advertiser.functions
        annotations = advertiser.functions["process_data"]["args"]

        # Verify the complex annotations are properly captured
        assert annotations["name"] == "process_data"
        assert len(annotations["args"]) == 2

        # Check first argument (List[Dict[str, Union[int, float]]])
        first_arg_type = annotations["args"][0][1]
        assert first_arg_type["type_name"] == "List"
        assert first_arg_type["args"]["type_name"] == "Dict"

    @patch("accioaudis_sdk.capture_function_annotations")
    def test_capture_function_annotations_called(self, mock_capture):
        """Test that capture_function_annotations is called when decorating"""
        advertiser = Advertiser()
        mock_capture.return_value = {"mock": "annotations"}

        @advertiser.search()
        def test_func(x: int) -> str:
            return "test"

        mock_capture.assert_called_once_with(test_func)
        assert advertiser.functions["test_func"]["args"] == {"mock": "annotations"}


class TestIntegration:
    """Integration tests combining multiple components"""

    def test_full_workflow(self):
        """Test the complete workflow from decoration to annotation capture"""
        advertiser = Advertiser()

        # Define functions with various type annotations
        @advertiser.search()
        def string_processor(text: str, count: int) -> List[str]:
            return [text] * count

        @advertiser.search()
        def data_processor(
            items: List[Dict[str, Any]], default: Union[str, int, None]
        ) -> Dict[str, List[Any]]:
            return {"result": items}

        # Verify both functions are registered
        assert len(advertiser.functions) == 2
        assert "string_processor" in advertiser.functions
        assert "data_processor" in advertiser.functions

        # Verify annotations are correctly captured
        string_proc_annotations = advertiser.functions["string_processor"]["args"]
        data_proc_annotations = advertiser.functions["data_processor"]["args"]

        assert string_proc_annotations["name"] == "string_processor"
        assert data_proc_annotations["name"] == "data_processor"

        # Test that the original functions still work
        assert string_processor("hello", 2) == ["hello", "hello"]


# Edge case tests
def test_edge_cases():
    """Test various edge cases"""
    advertiser = Advertiser()

    # Function with no parameters
    @advertiser.search()
    def no_params() -> str:
        return "constant"

    annotations = advertiser.functions["no_params"]["args"]
    assert annotations["args"] == []  # No arguments
    assert annotations["return_type"]["type_name"] == "str"

    # Function with *args and **kwargs
    @advertiser.search()
    def var_args(*args: str, **kwargs: int) -> None:
        pass

    # Note: *args and **kwargs will have their annotations captured normally
