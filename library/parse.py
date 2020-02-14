def parse_killfeed(frame):
    return frame[150:250, 1450:-100]


def parse_minimap(frame):
    return frame[45:300, 50:300]


def parse_playercount(frame):
    return frame[55:75, 1760:1782]


def parse_round(frame):
    return frame[340:360, 50:200]


def parse_clock(frame):
    return frame[335:360, 200:300]
