from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
from lib.parse import parse_minimap
from lib.stream import read_frames

master = cv2.imread('data/worldedge.png')
methods = [
    'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'
]

master = cv2.resize(master, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)


def crop_cimage(img, cropx, cropy):
    y, x = img.shape
    startx = x // 2 - (cropx // 2)
    starty = y // 2 - (cropy // 2)
    return img[starty:starty + cropy, startx:startx + cropx]


def show_img(img_to_show):
    plt.imshow(img_to_show)
    plt.show()


def stitch(images):
    stitcher = cv2.createStitcher()
    (status, stitched) = stitcher.stitch(images)
    if status == 0:
        return stitched
    else:
        raise Exception(f"Status: {status}")


def find_homo(img1, img2):
    MIN_MATCH_COUNT = 10
    MIN_DIST_THRESHOLD = 0.7
    RANSAC_REPROJ_THRESHOLD = 5.0
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < MIN_DIST_THRESHOLD * n.distance:
            good.append(m)
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt
                              for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt
                              for m in good]).reshape(-1, 1, 2)
        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,
                                  RANSAC_REPROJ_THRESHOLD)
        return H
    else:
        raise Exception("Not enough matches are found - {}/{}".format(
            len(good), MIN_MATCH_COUNT))


def warp(image, h):
    return cv2.warpPerspective(image, h, image.shape[:2])


def decompose(H,
              K=np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])):
    retrivials, rotations, translations, normals = cv2.decomposeHomographyMat(
        H, K)
    return translations[0][0][0], translations[0][1][0], math.acos(
        rotations[0][1, 1])


def extract_path(frames, initial=(0, 0, 0)):
    positions = [initial]
    previous = frames[0]
    for i in tqdm(range(1, len(frames))):
        try:
            h = find_homo(previous, frames[i])
            x1, y1, r1 = positions[-1]
            x2, y2, r2 = decompose(h)
            positions.append((x1 + x2, y1 + y2, r1 + r2))
            previous = frames[i]
        except Exception:
            positions.append(positions[-1])
    return positions


def plot_path(p):
    for x, y, r in p:
        plt.plot(x,
                 y,
                 marker=(3, 0, r * 180 / math.pi),
                 markersize=20,
                 linestyle='None')
        plt.pause(0.05)
    plt.show()


def find_template(img, template, meth='cv2.TM_CCORR'):
    img2 = img.copy()
    z, w, h = template.shape[::-1]
    img = img2.copy()
    method = eval(meth)
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    plt.subplot(121), plt.imshow(template, cmap='gray')
    plt.title('Template Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()


def read_and_plot():
    mm = read_frames(jump=10, limit=100, parser=parse_minimap)
    positions = extract_path(mm)
    plot_path(positions)
