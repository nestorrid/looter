import pytest
from looter import Item


def test_items_with_same_target_should_consider_equal():
    tar = []
    item1 = Item(tar)
    item2 = Item(tar)
    assert item1 == item2
    assert id(item1) != id(item2)


def test_none_target_should_get_is_empty_to_true():
    item = Item(None)
    assert item.is_empty


def test_two_empty_item_should_coinsider_equal():
    item1 = Item(None)
    item2 = Item(None)
    assert item1 == item2
