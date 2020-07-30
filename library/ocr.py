import pyocr
import pyocr.builders
from PIL import Image
import PIL.ImageOps
from pytesseract import image_to_string
import numpy as np


def its(image):
    inverted_image = PIL.ImageOps.invert(image.convert('RGB'))
    out_standard = image_to_string(image)
    out_inverted = image_to_string(inverted_image)
    return out_standard, out_inverted


def read_digits(im,inverted=True):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    if inverted:
        im = PIL.ImageOps.invert(im.convert('RGB'))
    tool = pyocr.get_available_tools()[0]
    builder = pyocr.builders.DigitBuilder()
    builder.tesseract_layout = 10
    builder.tesseract_flags = ['--psm', '10']
    return tool.image_to_string(im, lang="eng", builder=builder)

def read_text(im,inverted=True):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    if inverted:
        im = PIL.ImageOps.invert(im.convert('RGB'))
    tool = pyocr.get_available_tools()[0]
    builder = pyocr.builders.TextBuilder()
    return tool.image_to_string(im, lang="eng", builder=builder)


def read_lines(im,inverted=False):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    if inverted:
        im = PIL.ImageOps.invert(im.convert('RGB'))
    tool = pyocr.get_available_tools()[0]
    builder = pyocr.builders.LineBoxBuilder()
    return tool.image_to_string(im, lang="eng", builder=builder)

def read_boxes(im):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)

def read_boxes(im,inverted=False):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    if inverted:
        im = PIL.ImageOps.invert(im.convert('RGB'))
    tool = pyocr.get_available_tools()[0]
    builder = pyocr.builders.WordBoxBuilder()
    return tool.image_to_string(im, lang="eng", builder=builder)
