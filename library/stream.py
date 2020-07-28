import cv2
from .ocr import read_digits, read_lines, read_text
from .image import cap_data
from . import parse, interpret
from tqdm import tqdm
import pandas as pd


def process_video(filename='apex/data/tsm.6.02/Round1/nicewigg.mp4', fps=20):
    cap = cv2.VideoCapture(filename)
    cd = cap_data(cap)
    jump = cd['fps'] / fps
    frames = list()
    dim = [cd['width'], cd['height']]
    for i in tqdm(range(cd['frames'])):
        ret, frame = cap.read()
        if i % jump == 0 and ret:
            frame_data = {'i': i, 'time': cd['time'] * i / cd['frames']}
            parsed = parse_frame(frame, dim)
            frames.append({
                **frame_data,
                **process_frame(frame, dim), 'parsed': parsed
            })
    return frames


def process_frame(parsed):
    return {
        'killfeed': [k.content for k in read_lines(parsed['killfeed'])],
        'round': read_digits(parsed['round']),
        'clock': read_text(parsed['clock']),
        'playercount': read_digits(parsed['playercount']),
        'primary': read_text(parsed['primary']),
        'secondary': read_text(parsed['secondary'])
    }


def parse_frame(frame, dim=[1080, 1920]):
    return {
        x: getattr(parse, f'parse_{x}')(frame, dim)
        for x in [
            'killfeed', 'round', 'clock', 'playercount', 'minimap', 'primary',
            'secondary'
        ]
    }


def read_frames(filename='apex/data/tsm.6.02/Round1/nicewigg.mp4',
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


def parse_video(filename='apex/data/tsm.6.02/Round1/nicewigg.mp4',
                fps=20,
                n=0):
    cap = cv2.VideoCapture(filename)
    cd = cap_data(cap)
    frames = list()
    jump = cd['fps'] / fps
    dim = [cd['width'], cd['height']]
    for i in tqdm(range(int(n * jump) if n else cd['frames'])):
        ret, frame = cap.read()
        if i % jump == 0 and ret:
            frame_data = {
                'i': i,
                'time': cd['time'] * i / cd['frames'],
                'parsed': parse_frame(frame, dim),
                'raw': frame
            }
            frames.append(frame_data)
    return cd,frames


