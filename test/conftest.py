import pytest
from typing import List

from looter import ItemSet, Item, Looter


@pytest.fixture
def iset() -> ItemSet:
    return ItemSet()


@pytest.fixture
def names() -> list:
    return ['tom', 'jack', 'john', 'rose', 'bill']


@pytest.fixture
def nameset(iset, names) -> ItemSet:
    items = [Item(name) for name in names]
    iset.add_all(items)
    return iset


@pytest.fixture
def items() -> List[Item]:
    return [Item(f'fake-item-{i}', weight=0.1) for i in range(8)]


@pytest.fixture
def item() -> Item:
    return Item('fake-item', weight=0.2)


@pytest.fixture
def looter() -> Looter:
    return Looter()
