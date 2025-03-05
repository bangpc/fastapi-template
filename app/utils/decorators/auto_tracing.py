from app.utils.instrumentation import tracer
from functools import wraps


def auto_tracing():
    def decorator(func):
        def snake_to_camel(
            snake_str, 
            fist_capitalized = False
            ):
            """_summary_

            Args:
                snake_str (_type_): _description_
                fist_capitalized (bool, optional): _description_. Defaults to False.

            Returns:
                _type_: _description_
            """    
            # Split the string by underscores and capitalize each word except the first
            components = snake_str.split('_')
            if fist_capitalized:
                components[0] = components[0].capitalize()
            camel_case_str = components[0] + ''.join(word.capitalize() for word in components[1:])
            return camel_case_str

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Automatically get the function's module, class (if exists), and function name
            project = "Controller"
            module = "::".join([snake_to_camel(_, fist_capitalized=True) for _ in func.__module__.split(".")])
            class_name = func.__qualname__.split(".")[0] if "." in func.__qualname__ else None
            func_name = snake_to_camel(func.__name__, fist_capitalized=True)

            # Construct the path in the form module.ClassName.function_name or module.function_name
            path = f"{project}::{module}::{class_name}::{func_name}" if class_name else f"{module}::{func_name}"
            # Start the tracer span with the automatically determined path
            tracer.start_as_current_span(path)

            # Execute the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator