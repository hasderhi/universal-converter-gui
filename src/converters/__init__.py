import pkgutil
import importlib
import inspect
from .base import Converter

def load_converters():
    converters = []
    package = __name__
    for _, module_name, _ in pkgutil.iter_modules([__path__[0]]):
        if module_name == "base":
            continue
        module = importlib.import_module(f"{package}.{module_name}")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Converter) and obj is not Converter:
                converters.append(obj())
    return converters
