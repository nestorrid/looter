import pytest

from looter import funcs
from looter import Item


def test_total_weight_should_return_sum_of_item_weight_in_items():
    items = [Item(f'item{i}', weight=0.1) for i in range(8)]
    assert funcs.get_total_weight(items) == pytest.approx(0.8)


def test_probability_should_not_contain_zero(iset, items):
    prob = funcs.get_probability(items)
    assert prob.count(0) == 0
    assert prob.count(items[0].weight) == len(items)
