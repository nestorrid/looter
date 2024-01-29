from __future__ import annotations
from dataclasses import dataclass
from typing import Union, List, Generic, Any, Tuple
import typing
from random import choices, randint
from collections import namedtuple

from looter import funcs


class Item:

    def __init__(self, target: Generic[Any], weight=0):
        self.weight = weight
        self.target = target

    @staticmethod
    def empty(weight: float = 0):
        return Item(None, weight)

    @property
    def is_empty(self):
        return self.target is None

    def __eq__(self, other: Item) -> bool:
        if not isinstance(other, Item):
            return False

        if self.is_empty:
            return other.is_empty

        return id(self.target) == id(other.target)

    def __str__(self) -> str:
        target = hex(id(self.target))
        if self.is_empty:
            target = 'EMPTY'
        return f"Item(target={target}, weight={self.weight})"

    def __repr__(self) -> str:
        return str(self)


class ItemSet:

    def __init__(self, weight: float = 0, loot_count=1, max_loot_count=0):
        self.items: List[Item] = list()
        self.weight = weight
        self.loot_count = loot_count
        self.max_loot_count = max_loot_count

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'ItemSet(count={len(self.items)}, weight={self.weight})'

    @classmethod
    def empty(cls, weight: float = 0):
        return cls(weight=weight)

    def add(self, item: Item):
        if self.items.count(item) == 0:
            self.items.append(item)

    def add_all(self, items: List[Item]):
        for item in items:
            self.add(item)

    @property
    def is_empty(self):
        return len(self.items) == 0

    def __eq__(self, other) -> bool:
        if self.is_empty or not isinstance(other, ItemSet):
            return False
        return self.items == other.items

    @property
    def count(self):
        return len(self.items)

    def loot(self, count=0, unique=False) -> List[Item]:

        if len(self.items) == 0:
            return [Item.empty()]

        if unique:
            funcs.raise_if_not_enough_unique_items(count, self.items)

        loot_count = count if count > 0 else self.loot_count

        if self.max_loot_count > 0:
            loot_count = randint(
                min(loot_count, self.max_loot_count),
                self.max_loot_count
            )

        items = []
        while len(items) < loot_count:
            item = choices(self.items, funcs.get_probability(self.items))[0]
            if unique and not item.is_empty and items.count(item) > 0:
                continue
            items.append(item)

        return items


LootContainer = namedtuple(
    'LootContainer', ['default', 'addtional'], defaults=[List, List])


@dataclass
class LootConfig:

    loot_count: int = 2
    max_loot_coount: int = 0
    unique: bool = True
    can_be_empty: bool = True


class Looter:

    def __init__(self, config: LootConfig = LootConfig()):
        self.config = config
        self._items = LootContainer([], [])

    def add(self, item: Union[ItemSet, Item], *, additional=False):
        if additional:
            self._items.addtional.append(item)
        else:
            self._items.default.append(item)

    def add_all(self, items: List[Union[ItemSet, Item]], *, additional=False):
        for item in items:
            self.add(item, additional=additional)

    @property
    def default_items(self) -> List[Union[ItemSet, Item]]:
        return self._items.default

    @property
    def additional_items(self) -> List[Union[ItemSet, Item]]:
        return self._items.addtional

    @property
    def count(self):
        return self.default_count + self.additional_count

    @property
    def default_count(self):
        return len(self._items.default)

    @property
    def additional_count(self):
        return len(self._items.addtional)

    def _get_empty_item(self, default=True) -> List[Item]:
        target = self.default_items if default else self.additional_items
        prob = 1 - funcs.get_total_weight(target)
        if prob < 0:
            return []
        return [Item.empty(weight=prob)]

    def _get_loot_count(self, config: LootConfig):
        count = config.loot_count
        if config.unique:
            funcs.raise_if_not_enough_unique_items(count, self.default_items)

        if config.max_loot_coount > 0:
            count = randint(min(count, config.max_loot_coount),
                            config.max_loot_coount)
        return count

    def _get_loot_list(self, config: LootConfig):
        items = self.default_items[:]

        if config.can_be_empty:
            items.extend(self._get_empty_item())

        return items

    def _get_item_or_loot_from_itemset(self, target: Union[Item, ItemSet]) -> List[Item]:
        if isinstance(target, Item):
            return [target]

        if isinstance(target, ItemSet):
            return target.loot()

    def _get_additional_results(self):
        if self.additional_count == 0:
            return []

        source = self.additional_items[:]
        source.extend(self._get_empty_item(default=False))
        prob = funcs.get_probability(source)
        return choices(source, prob)

    def loot(self, config: LootConfig = None) -> List[Item]:
        conf = config or self.config
        count = self._get_loot_count(conf)

        items = self._get_loot_list(conf)
        prob = funcs.get_probability(items)

        results = []
        while len(results) < count:
            item_list = self._get_item_or_loot_from_itemset(
                choices(items, prob)[0])
            for i in item_list:
                if conf.unique and not i.is_empty and results.count(i) > 0:
                    continue
                results.append(i)

        results.extend(self._get_additional_results())
        return [
            item for item in results
            if not item.is_empty
        ]

    def loot_scalars(self, config: LootConfig = None) -> List[Any]:
        return [item.target for item in self.loot(config)]

    def _loot_addtional_items(self) -> List[Item]:
        if self.additional_count == 0:
            return []

        loot = self.additional_items[:]
        loot.extend(self._get_empty_item(default=False))
        prob = funcs.get_probability(loot)
        item = choices(loot, prob)[0]
        if item.is_empty:
            return []

        return [item]
