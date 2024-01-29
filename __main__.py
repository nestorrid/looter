from typing import List
from looter import Item, ItemSet, Looter


def equip_set() -> ItemSet:
    equip_set = ItemSet(weight=0.4)
    names = ['武器', '头盔', '护手', '胸甲', '护腿']
    equip_set.add_all([Item(name, weight=0.1) for name in names])
    return equip_set


def material_set() -> ItemSet:
    met_set = ItemSet(weight=0.3, max_loot_count=5)
    names = ['亚麻布', '毛料', '丝绸', '魔纹布', '符文布']
    met_set.add_all([
        Item(name, weight=0.1) for name in names
    ])
    return met_set


if __name__ == "__main__":
    looter = Looter()
    looter.add_all([equip_set(), material_set()])
    looter.config.loot_count = 2
    result = looter.loot_scalars()
    print(result)
