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


def read_digits(im):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    tool = pyocr.get_available_tools()[0]
    builder = pyocr.builders.DigitBuilder()
    builder.tesseract_layout = 10
    builder.tesseract_flags = ['--psm', '10']
    return tool.image_to_string(im, lang="eng", builder=builder)


def read_text(im):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    tool = pyocr.get_available_tools()[0]
    builder = pyocr.builders.TextBuilder()
    return tool.image_to_string(im, lang="eng", builder=builder)


def read_lines(im):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    tool = pyocr.get_available_tools()[0]
    builder = pyocr.builders.LineBoxBuilder()
    return tool.image_to_string(im, lang="eng", builder=builder)


def read_boxes(im):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(im)
    tool = pyocr.get_available_tools()[0]
    builder = pyocr.builders.WordBoxBuilder()
    return tool.image_to_string(im, lang="eng", builder=builder)
