import types

def is_serializable(v):
    return not callable(v) and not isinstance(v, types.ModuleType)


def make_serializable(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {str(k): make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, types.ModuleType):
        return f"<module {getattr(obj, '__name__', str(obj))}>"
    elif callable(obj):
        return f"<function {getattr(obj, '__name__', str(obj))}>"
    else:
        return f"<non-serializable {type(obj).__name__}>"
