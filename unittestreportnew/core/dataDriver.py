from functools import wraps


def _create_test_name(index, name, title):
    """
    Create a new test name based on index and name.
    :param index: Index for generating the test name.
    :param name: Base name for the test.
    :param title: Base title for the test.
    :return: Generated test name.
    """
    test_name = f"{name}_{index + 1:03}_{title}"
    return test_name


def _set_function_attributes(func, original_func, new_name, test_desc):
    """
    Set attributes of a function.
    :param func: The function to set attributes for.
    :param original_func: The original function being wrapped.
    :param new_name: New name for the function.
    :param test_desc: New documentation for the function.
    """
    func.__wrapped__ = original_func
    func.__name__ = new_name
    func.__doc__ = test_desc


def _update_func(new_func_name, params, test_desc, func, *args, **kwargs):
    """
    Create a wrapper function with updated attributes.
    :param new_func_name: New name for the wrapper function.
    :param params: Test parameters.
    :param test_desc: Test description.
    :param func: Original function to be wrapped.
    :param args: Additional positional arguments for the function.
    :param kwargs: Additional keyword arguments for the function.
    :return: Wrapped function.
    """

    @wraps(func)
    def wrapper(self):
        return func(self, params, *args, **kwargs)

    _set_function_attributes(wrapper, func, new_func_name, test_desc)
    return wrapper


def ddt(cls):
    """
    :param cls: 测试类
    :return:
    """
    for func_name, func in list(cls.__dict__.items()):
        if hasattr(func, "PARAMS"):
            for index, case_data in enumerate(getattr(func, "PARAMS")):
                name = str(case_data.get("Name", "缺少Name"))
                test_desc = str(case_data.get("Description", "缺少Description"))
                new_test_name = _create_test_name(index, func_name, name)
                func2 = _update_func(new_test_name, case_data, test_desc, func)
                setattr(cls, new_test_name, func2)
            else:
                # Avoid name clashes
                delattr(cls, func_name)
    return cls
