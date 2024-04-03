from collections.abc import MutableMapping


def add_numeration_to_response(queryset: list[MutableMapping]) -> dict:
    result = {}
    for n in range(len(queryset)):
        result[str(n)] = queryset[n]

    return result
