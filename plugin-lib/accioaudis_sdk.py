import inspect
from typing import Any, Dict, Union, get_origin, get_args


class Advertiser:
    functions: Dict

    def __init__(self) -> None:
        self.functions = {}

    def search(self):
        def decorator(func):
            self.functions[func.__name__] = {
                "function": func,
                "args": capture_function_annotations(func),
            }
            return func

        return decorator


def analyze_annotation(annotation: Any) -> Dict[str, Any]:
    if get_origin(annotation) is Union:
        return {
            "type_name": "Union",
            "args": [analyze_annotation(arg) for arg in get_args(annotation)],
        }
    elif get_origin(annotation) is list:
        return {
            "type_name": "List",
            "args": analyze_annotation(get_args(annotation)[0]),
        }
    elif get_origin(annotation) is dict:
        return {
            "type_name": "Dict",
            "args": analyze_annotation(get_args(annotation)[0]),
            "values": analyze_annotation(get_args(annotation)[1]),
        }

    elif annotation is None:
        return {"type_name": "None"}
    else:
        return {"type_name": annotation.__name__}


def capture_function_annotations(func: Any) -> Dict[str, Any]:
    # Get the signature of the function
    sig = inspect.signature(func)

    # Extract the parameter names and types
    args = [
        (param.name, analyze_annotation(param.annotation))
        for param in sig.parameters.values()
    ]

    # Get the return type
    return_type = analyze_annotation(sig.return_annotation)

    # Create a dictionary to hold the annotations
    annotation = {"name": func.__name__, "args": args, "return_type": return_type}

    return annotation
