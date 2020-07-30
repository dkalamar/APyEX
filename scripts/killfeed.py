import jellyfish as jfish
import re
import pandas as pd
from ..library import interpret

def run():
    rounds = pd.read_csv('apex/data/player_rounds.csv')
    rounds = rounds.set_index(rounds.columns[0])
    rounds.index = rounds.index.str.upper()
    df = pd.concat([examine(i,rounds['Round 1']) for i in range(1, 6)])
    return df


def examine(i,r):
    self = Round(f'apex/data/killfeed/algs_round_{i}',
                 r.str.upper().to_dict())
    self.parse_lines()
    self.match_items()
    return self.events


class Round:
    def __init__(self, path, player_dict):
        self.players = player_dict
        self.path = path
        self.weapons = {
            'R-99', 'R-301', 'HEMLOK', 'MASTIFF', 'EVA-8', 'HAVOC', 'RE-45',
            'G7 SCOUT', 'CHARGE RIFLE', 'ARC STAR', 'GRENADE', 'THERMITE',
            'TRIPLE TAKE', 'P2020', 'MOZAMBIQUE', 'LONGBOW', 'SENTINEL',
            'KRABER', 'PEACEKEEPER', 'DEFENSIVE BOMBARDMENT', 'BOMBARD',
            'PROWLER', 'FLATLINE', 'DEVOTION', 'SPITFIRE','WINGMAN','LSTAR',
            'ALTERNATOR'
        }
        self.actions = {'BLEED OUT', 'DEFENSIVE BOMBARDMENT', 'RING', 'MELEE','FINISHER'}
        self.events = pd.DataFrame()

    def parse_lines(self):
        fp = open(self.path, 'r')
        self.events = pd.DataFrame(list(map(interpret.killfeed_line, fp.readlines())))
        fp.close()

    def match_items(self):
        compare_dict = {
            'killer': self.players.keys(),
            'target': self.players.keys(),
            'action': self.actions,
            'weapon': self.weapons
        }
        for column, comparison in compare_dict.items():
            self.events[f'matched_{column}'] = self.events[column].apply(
                lambda a: self._match_item(a, comparison))
        self.events['legend_killer'] = self.events['matched_killer'].apply(
            self.players.get)
        self.events['legend_target'] = self.events['matched_target'].apply(
            self.players.get)

    def _match_item(self, item, compare, cutoff=.5):
        if not item:
            return None
        results = list(map(lambda a: jfish.jaro_distance(item, a), compare))
        res = max(results)
        return list(compare)[results.index(res)] if res >= cutoff else '????'
