from typing import List, Union
from functools import reduce
# from looter import Item, ItemSet


def get_probability(items: List) -> List[float]:
    prob = [item.weight for item in items]
    total_weight = get_total_weight(items)

    if total_weight > 1:
        raise ValueError(
            """
            Total item weight should less than '1.0'. But get '%.2f'.
            """ % total_weight
        )

    zeros = prob.count(0)
    if zeros > 0:
        weight = (1 - total_weight) / zeros
        for index, v in enumerate(prob):
            if prob[index] == 0:
                prob[index] = weight

    return prob


def raise_if_not_enough_unique_items(count, items: List):
    if count > len(items):
        raise ValueError(
            f"""
            Loot count({count!r}) is greater than total item count({len(items)!r}) in this ItemSet.
            can not loot an unique list of items.
            
            Try less item count or set `unique=False`.
            """
        )


def get_total_weight(items: List) -> float:
    weights = [item.weight for item in items]
    return reduce(
        lambda x, y: x + y,
        weights
    )
