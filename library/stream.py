import cv2
from .ocr import read_digits, read_lines, read_text
from .image import cap_data
from . import parse
from tqdm import tqdm


def process_video(filename='apex/dataace_test.mp4', fps=20):
    cap = cv2.VideoCapture(filename)
    cd = cap_data(cap)
    jump = cd['fps'] / fps
    frames = list()
    for i in tqdm(range(cd['count'])):
        ret, frame = cap.read()
        if i % jump == 0 and ret:
            frame_data = {'i': i, 'time': cd['time'] * i / cd['count']}
            frames.append({**frame_data, **process_frame(frame)})
    return frames


def process_frame(frame):
    parsed = parse_frame(frame)
    return {
        'killfeed': [k.content for k in read_lines(parsed['killfeed'])],
        'round': read_text(parsed['round']),
        'clock': read_digits(parsed['clock']),
        'playercount': read_digits(parsed['playercount']),
        'image': parsed
    }


def parse_frame(frame):
    return {
        x: getattr(parse, f'parse_{x}')(frame)
        for x in ['killfeed', 'round', 'clock', 'playercount', 'minimap']
    }


def read_frames(filename='dataace_test.mp4',
                jump=1,
                limit=100000,
                parser=lambda a: a):
    cap = cv2.VideoCapture(filename)
    i = 0
    ret = True
    frames = list()
    while ret and cap.isOpened() and len(frames) < limit:
        print(i, end='\r')
        ret, frame = cap.read()
        if i % jump == 0:
            frames.append(parser(frame))
        i += 1
    return frames
