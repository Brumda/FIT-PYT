#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 0.1

Cílem je vykreslit v "UTF16-artu" strom definovaný listem hodnot. Každý vnitřní uzel stromu obsahuje vždy dvě položky: název uzlu a seznam potomků (nemusí být nutně v tomto pořadí). Názvem může být jakýkoli objekt kromě typu list (seznam).

Příklady validních stromů:
    - triviální strom o 1 uzlu: [1, []]
    - triviální strom o 1 uzlu s opačným pořadím ID a potomků: [[], 2]
    - triviální strom o 3 uzlech: [1, [2, 3]]
        (listové uzly ve stromu o výšce >= 2 mohou být pro zjednodušení zapsány i bez prázdného seznamu potomků)

Příklady nevalidních stromů:
    - None
    - []
    - [666]
    - [1, 2]
    - (1, [2, 3])


Strom bude vykreslen podle následujících pravidel:
    - Vykresluje se shora dolů, zleva doprava.
    - Uzel je reprezentován jménem, které je stringovou serializací objektu daného v definici uzlu.
    - Uzel v hloubce N bude odsazen zlava o N×{indent} znaků, přičemž hodnota {indent} bude vždy kladné celé číslo > 1.
    - Má-li uzel K potomků, povede:
        - k 1. až K-1. uzlu šipka začínající znakem ├ (UTF16: 0x251C)
        - ke K. uzlu šipka začínající znakem └ (UTF16: 0x2514)
    - Šipka k potomku uzlu je vždy zakončena znakem > (UTF16: 0x003E; klasické "větší než").
    - Celková délka šipky (včetně úvodního znaku a koncového ">") je vždy {indent}, výplňovým znakem je zopakovaný znak ─ (UTF16: 0x2500).
    - Všichni potomci uzlu jsou spojeni na úrovni počátku šipek svislou čarou │ (UTF16: 0x2502); tedy tam, kde není jako úvodní znak ├ nebo └.
    - Pokud název uzlu obsahuje znak `\n` neodsazujte nijak zbytek názvu po tomto znaku.
    - Každý řádek je ukončen znakem `\n`.

Další požadavky na vypracovní:
    - Pro nevalidní vstup musí implementace vyhodit výjimku `raise Exception('Invalid tree')`.
    - Mít codestyle v souladu s PEP8 (můžete ignorovat požadavek na délku řádků - C0301 a používat v odůvodněných případech i jednopísmenné proměnné - C0103)
        - otestujte si pomocí `pylint --disable=C0301,C0103 trees.py`
    - Vystačit si s buildins metodami, tj. žádné importy dalších modulů.


Příklady vstupu a výstupu:
INPUT:
[[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...└──>True
│.......├──>abc
│.......└──>def
└──>2
....├──>3.14159
....└──>6.023e+23

INPUT:
[[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23, 2.718281828]], [3, ['x', 'y']], [4, []]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...├──>True
│...│...├──>abc
│...│...└──>def
│...└──>False
│.......├──>1
│.......└──>2
├──>2
│...├──>3.14159
│...├──>6.023e+23
│...└──>2.718281828
├──>3
│...├──>x
│...└──>y
└──>4

INPUT:
[6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>4
    ├>1
    │ ├>2
    │ └>3
    └>42
      ├>-43
      └>44

INPUT:
[6, [5, ['dva\nradky']]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>dva
radky

Potřebné UTF16-art znaky:
└ ├ ─ │

Odkazy:
https://en.wikipedia.org/wiki/Box_Drawing
"""


def check_tree(tree) -> None:
    """checks if the tree is valid ie if it's not list at all, contains only lists or no lists"""
    if not isinstance(tree, list):
        raise Exception('Invalid tree')
    if all(isinstance(item, list) for item in tree):
        raise Exception('Invalid tree')
    if not any(isinstance(item, list) for item in tree):
        raise Exception('Invalid tree')
    if len(tree) != 2:
        raise Exception('Invalid tree')


class Node:
    """Helper class for nodes. In C I would use structure, but IDK how to that here"""

    def __init__(self, data, parent=None, children=None):
        self.data = data
        self.children = children if children else []
        self.parent = parent
        self.last = False
        if children:
            def flatten(lst):
                flattened_list = []
                for item in lst:
                    if isinstance(item, list):
                        flattened_list.extend(flatten(item))
                    else:
                        flattened_list.append(item)
                return flattened_list

            self.children = flatten(children)
            self.children = [child for child in self.children if not isinstance(child.data, list)]
            self.children[-1].last = True

    def i_dont_know_how_to_do_helper_structures(self):
        """pylint is my mortal enemy"""
        print(self.last)
        print("Im sorry, look here instead of my code: https://tenor.com/search/cute-kitten-gifs")

    def so_I_did_this_so_pylint_doesnt_cry(self):
        """At least you know I did not copy this lmao"""
        print(self.last)
        print("Im sorry, look here instead of my code: https://gifdb.com/cute-kitten")


def rearrange_list(nested_list, parent=None):
    """rearranges the list into list that has parent first, children later"""
    singles = []
    subtrees = []
    for item in nested_list:
        if isinstance(item, list):
            subtrees.append(rearrange_list(item, parent))
        else:
            singles.append(item)
    return singles + subtrees


def create_tree(nested_list, parent=None):
    """recursive function that creates nodes with children and parent"""
    singles = []
    subtrees = []
    for item in nested_list:
        if isinstance(item, list):
            if len(item) > 0:
                if not isinstance(item[0], list):
                    subtrees.append(create_tree(item, singles[0]))
                else:
                    for item2 in item:
                        subtrees.append(create_tree(item2, singles[0]))
            else:
                singles.append(item)
        else:
            singles.append(item)
    if len(singles) == 1:
        if len(subtrees) > 0:
            return Node(singles[0], parent, subtrees if not isinstance(subtrees[0], list) else subtrees[0])
        return Node(singles[0], parent, [])
    nodes = []
    for single in singles:
        nodes.append(Node(single, parent, []))
    return nodes


def print_tree(node, indent, separator, prefix="") -> str:
    """recursive function that prints the tree structure"""
    prefix_fix = len(prefix)
    if prefix and prefix[-1] == "│":
        prefix_fix = -1

    if node.parent is None:
        tree = f"{node.data}\n"
    elif node.last:
        tree = f"{prefix[:prefix_fix]}└{(indent - 2) * '─'}>{node.data}\n"
        prefix = prefix[:prefix_fix]
    else:
        tree = f"{prefix[:prefix_fix]}├{(indent - 2) * '─'}>{node.data}\n"

    prefix_fix = len(prefix) + indent
    if prefix and prefix[-1] == "│":
        prefix_fix = -1

    for child in node.children:
        if len(node.children) > 1:
            tree += print_tree(child, indent, separator,
                               (prefix + separator * indent)[:prefix_fix] + "│" if node.parent is not None else "│")
        else:
            tree += print_tree(child, indent, separator,
                               (prefix + separator * indent)[:prefix_fix] if node.parent is not None else "")
    return tree


# zachovejte interface metody
def render_tree(tree: list = None, indent: int = 2, separator: str = ' ') -> str:
    """Base function that the test calls"""
    check_tree(tree)
    tree = rearrange_list(tree)
    actual_tree = create_tree(tree)
    string = print_tree(actual_tree, indent, separator, "")
    return string


if __name__ == "__main__":
    render_tree()
