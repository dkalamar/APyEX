from ..library.stream import read_text, parse_video, parse_frame
from ..library import interpret
from ..library.image import save_img
from ..engine.VideoStreamer import VideoStreamer
from tqdm import tqdm
from glob import glob
import json
import sys
import datetime


def read_weapons(frames):
    w = [(read_text(f['parsed']['primary']),
          read_text(f['parsed']['secondary'])) for f in tqdm(frames)]
    return interpret.inventory(w)

def stream(link,save_file):
    vs = VideoStreamer(link,live=True)
    inv = ['','']
    f=open(f'apex/data/log/{save_file}.txt','w',encoding='utf-8')
    i=0
    try:
        while True:
            frame = vs.read()
            parsed = parse_frame(frame,[720,1280])
            p,s = read_text(parsed['primary']),read_text(parsed['secondary'])
            reading = interpret._compare_inv(p, inv[0]), interpret._compare_inv(s, inv[1])
            print(','.join(reading)+'   ',end='\r')
            if reading != inv:
                f.write(','.join([str(datetime.datetime.now()),*reading])+'\n')
                inv = reading
                print('\n')
                save_img(frame,f'apex/data/frame_cache/{save_file}_{i}.png')
                i+=1
    except Exception as err:
        print(f'Error: {err}')
    finally:
        f.close()
        vs.stop()

def run(path):
    print("Parsing")
    cd, frames = parse_video(path, jump=100)
    print("Reading")
    cd['inventory'] = read_weapons(frames)
    print("Saving")
    save_file = path.split('/')[-1].split('.')[0]
    cd['path'] = path
    with open(f'apex/data/log/{save_file}.json','w') as fp:
        json.dump(cd,fp,indent=4)

def run_all(dir_path):
    paths=glob(dir_path)
    for p in paths:
        run(path)

if __name__ == "__main__":
    run_all(sys.argv[1])