import cv2
import matplotlib.pyplot as plt


def cap_data(cap):
    return {
                'height': int(cap.get(3)),
                'width': int(cap.get(4)),
                'fps': int(cap.get(cv2.CAP_PROP_FPS)),
                'frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'time': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / int(cap.get(cv2.CAP_PROP_FPS))
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


def crop_cimage(img, cropx, cropy):
    y, x = img.shape
    startx = x // 2 - (cropx // 2)
    starty = y // 2 - (cropy // 2)
    return img[starty:starty + cropy, startx:startx + cropx]


def show_img(img_to_show):
    plt.imshow(img_to_show)
    plt.show()
