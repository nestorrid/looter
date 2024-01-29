import pytest
from looter import Looter, ItemSet, Item, LootConfig
from looter.funcs import get_total_weight


def test_looter(looter):
    assert looter.count == 0


def test_add_item_will_into_default_items(looter, item):
    looter.add(item)
    assert looter.count == 1
    assert looter.default_count == 1
    assert looter.default_items[0] == item


def test_add_additional_items_will_into_additional_items(looter, item):
    looter.add(item, additional=True)
    assert looter.count == 1
    assert looter.additional_count == 1
    assert looter.additional_items[0] == item


def test_add_items_will_put_in_right_list(looter, items):
    looter.add_all(items)
    looter.add_all(items, additional=True)

    assert looter.count == len(items) * 2
    assert looter.default_items == items
    assert looter.additional_items == items


def test_get_loot_list(looter, items):
    looter.add_all(items)
    result = looter._get_loot_list(looter.config)
    assert len(result) == len(items) + 1
    assert result.count(Item.empty(0)) == 1


def test_get_loot_count_with_max_count_should_get_random_int_between_count_and_max(items):
    config = LootConfig(loot_count=2, max_loot_coount=5)
    looter = Looter(config)
    looter.add_all(items)
    for i in range(50):
        count = looter._get_loot_count(config)
        assert 2 <= count <= 5


def test_get_unique_loot_count_with_gt_item_count_should_raise_value_error(looter, items):
    looter.add_all(items)
    with pytest.raises(ValueError) as e:
        result = looter._get_loot_count(LootConfig(loot_count=10, unique=True))

    assert e.type == ValueError


def test_default_loot_should_get_two_items(looter, items):
    looter.add_all(items)
    looter.config.can_be_empty = False
    result = looter.loot()
    assert len(result) == 2


def test_itemset_in_loot_result_will_loot_one_item_in_itemset(looter, nameset, names):
    nameset.weight = 1
    looter.add(nameset)
    looter.config.loot_count = 1
    result = looter.loot_scalars()[0]
    assert names.count(result) == 1


def test_loot_scalars_should_get_list_of_item_target_list(looter, items):
    looter.add_all(items)
    looter.config.can_be_empty = False
    results = looter.loot_scalars()
    for result in results:
        assert type(result) == type(items[0].target)


def test_loot_source_should_contains_empty_item_if_can_be_empty(looter, items):
    looter.add_all(items)
    looter.config.can_be_empty = True
    source = looter._get_loot_list(looter.config)
    assert len(source) == len(items) + 1
    assert source.count(Item.empty()) > 0


def test_loot_source_should_be_same_with_original_list(looter, items):
    looter.add_all(items)
    looter.config.can_be_empty = False
    source = looter._get_loot_list(looter.config)
    assert source == items


def test_loot_should_get_additional_item_by_probability(looter):
    looter.add_all([Item(f'fake_item_{i}', weight=0.1) for i in range(3)])
    looter.add(Item('additional item', weight=1), additional=True)
    looter.config.loot_count = 2
    for i in range(10):
        result = looter.loot_scalars()
        assert 0 < len(result) <= 3
        assert result.count('additional item') == 1
