from typing import Any, List


def count_of_entry(list: List[Any], el: Any) -> int:
    
    count = 0
    for i in list:
        if i == el: count += 1

    return count