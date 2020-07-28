import itertools
import numpy as np
import jellyfish as jfish

weapons = [
    'ALTERNATOR', 'CHARGE RIFLE', 'DEVOTION', 'EVA-8', 'G7 SCOUT', 'HAVOC',
    'HEMLOK', 'KRABER', 'LONGBOW', 'L-STAR', 'MASTIFF', 'MOZAMBIQUE', 'P2020',
    'PEACEKEEPER', 'PROWLER', 'R-301', 'R-99', 'RE-45', 'SENTINEL', 'SPITFIRE',
    'TRIPLE TAKE', 'FLATLINE', 'WINGMAN', 'RETURN TO LOBBY'
]
common_errors = {"WASTIRR": "MASTIFF", ")CHAVOG:": "HAVOC"}


def inventory(w):
    inv = [(None, None)]
    for i in range(len(w)):
        p, s = list(map(lambda a: a.upper(), w[i]))
        f = _compare_inv(p, inv[-1][0]), _compare_inv(s, inv[-1][1])
        if f != inv[-1]:
            inv.append(f)
    return inv


def _compare_inv(f, o=None):
    if not f or (o and jfish.jaro_distance(f, o) > .75):
        return o
    if f not in weapons:
        f = common_errors.get(f, f)
        sim = [jfish.jaro_distance(f, w) for w in weapons]
        m = max(sim)
        if m > .75:
            f = weapons[sim.index(m)]
        else:
            return o
    return f