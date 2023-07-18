from .util import Inspect

def classify(inspect: Inspect) -> str:
    assert (inspect.category is None)
    inspect.category = "未知"
    return inspect.category
