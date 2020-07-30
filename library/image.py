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

def crop_cimage(img, cropx, cropy):
    y, x = img.shape
    startx = x // 2 - (cropx // 2)
    starty = y // 2 - (cropy // 2)
    return img[starty:starty + cropy, startx:startx + cropx]


def show_img(img_to_show):
    plt.imshow(img_to_show)
    plt.show()

def save_img(im,path):
    plt.imsave(path,im)
