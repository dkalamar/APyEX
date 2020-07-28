from library.stream import read_frames
from library.ocr import read_text
from library.parse import parse_killfeed


def pull_killfeed():
    kf = read_frames(jump=100, limit=1000000, parser=parse_killfeed)
    kf_text = list(map(read_text, kf))
