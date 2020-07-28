from ..library.stream import parse_video, parse_frame,process_frame
from ..library.image import save_img
from ..engine.VideoStreamer import VideoStreamer
import re
import pandas as pd
import os
from tqdm import tqdm
from glob import glob
import json
import sys
import datetime
import cv2

gll = {
    'senoxe': 'https://www.twitch.tv/videos/675002340',
    'snip3down': 'https://www.twitch.tv/videos/675014006',
    'ImMadness': 'https://www.twitch.tv/videos/675004921',
    'joeyblackout': 'https://www.twitch.tv/videos/675015718',
    'dropped': 'https://www.twitch.tv/videos/675010680',
    'bowswer': 'https://www.twitch.tv/videos/675012565',
    'nicewigg': 'https://www.twitch.tv/videos/668299079'
}

algs = {
    'gentrifyinq': 'https://www.twitch.tv/videos/678097453',
    'albralelie': 'https://www.twitch.tv/videos/677920243',
    'nicewigg': 'https://www.twitch.tv/videos/677915077',
    'snip3down': 'https://www.twitch.tv/videos/677926948',
    'dezignful': 'https://www.twitch.tv/videos/678092006',
    'lou': 'https://www.twitch.tv/videos/678084587',
    'nafen': 'https://www.twitch.tv/videos/678022881',
    'nokokopuffs': 'https://www.twitch.tv/videos/677914990',
    'frexs': 'https://www.twitch.tv/videos/677923671',
    'rockerapex': 'https://www.twitch.tv/videos/677607692'
}


def save_parsed(parsed, save_name, i):
    for k, v in parsed.items():
        save_img(
            v, f"apex/data/frame_cache/{k}/{save_name}_{str(i).zfill(8)}.png")


def stream(link, save_name, skip=1):
    vs = VideoStreamer(link, live=True)
    inv = ['', '']
    i = 0
    k = 0
    try:
        while True:
            frame = vs.read()
            if i % skip == 0:
                parsed = parse_frame(frame, [720, 1280])
                save_parsed(parsed, save_name, k)
                k += 1
            i += 1
    except Exception as err:
        print(f'Error: {err}')
    finally:
        vs.stop()


from glob import glob


def get_names(target='primary'):
    ls = glob(f'apex/data/frame_cache/{target}/*')
    return {re.findall(target + r'/(.*)_\d{8}', path)[0] for path in ls}


def analyze():
    names = get_names()
    for n in names:
        print(f'Running {n}...')
        try:
            parsed = pd.DataFrame(form_parse(n))
            results = [process_frame(r) for i,r in parsed.iterrows()]
            pd.DataFrame(results).to_json(f'apex/data/log/{n}.json')
        except Exception as err:
            print(f"{n} failed: {str(err)}")



def form_parse(name):
    ls = glob(f'apex/data/frame_cache/*/{name}_0*')
    parsed = dict()
    for path in ls:
        type_ = re.findall(r'frame_cache/(.*?)/', path)[0]
        if parsed.get(type_):
            parsed[type_].append(cv2.imread(path))
        else:
            parsed[type_] = [cv2.imread(path)]
    return parsed
