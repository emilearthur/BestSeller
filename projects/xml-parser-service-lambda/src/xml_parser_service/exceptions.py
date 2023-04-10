def format_exception(exception: Exception) -> str:  # pragma: no cover
    return f"{type(exception).__name__}: {' '.join([str(a) for a in exception.args if hasattr(a, '__str__')])}"
