from collections.abc import MutableMapping
from typing import List, Dict

def add_numeration_to_response(queryset: List[MutableMapping]) -> Dict:
    result = {}
    for n in range(len(queryset)):
        result[str(n)] = queryset[n]

    return result
