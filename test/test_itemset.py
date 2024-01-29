import pytest
from looter import Item, ItemSet


def test_loot_10_unique_items_will_raise_value_error(nameset):
    with pytest.raises(ValueError) as e:
        nameset.loot(10, unique=True)
    assert e.type == ValueError


def test_loot_10_items_will_get_item_list(nameset):
    result = nameset.loot(10, unique=False)
    assert len(result) == 10


def test_loot_with_max_loot_count_will_get_random_length_list(nameset):
    nameset.max_loot_count = 10
    result = nameset.loot(unique=False)
    assert len(result) > 0


@pytest.mark.parametrize('count', [5, 8, 10])
def test_loot_more_then_max_loot_count_will_always_get_max_count_length_list(nameset, count):
    nameset.max_loot_count = 3
    result = nameset.loot(count=count, unique=False)
    assert len(result) == 3


def test_loot_one_should_get_one_item(nameset, names):
    name = nameset.loot()
    assert len(name) == 1
    assert names.index(name[0].target) != -1


def test_total_weight_gt_one_should_raise_value_error(iset):
    items = [Item(f'item-{i}', weight=0.3) for i in range(5)]
    iset.add_all(items)

    with pytest.raises(ValueError) as e:
        iset.loot()

    assert e.type == ValueError


def test_add_one_item_should_get_length_one(iset):
    iset.add(Item("test"))
    assert iset.count == 1


def test_add_same_item_should_get_length_one(iset):
    item1 = Item('a')
    item2 = Item('a')
    iset.add_all([item1, item2])
    assert iset.count == 1


def test_add_two_items_should_get_length_two(iset):
    iset.add_all([Item('a'), Item('b')])
    assert iset.count == 2
