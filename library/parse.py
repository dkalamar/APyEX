import numpy as np

ui_mapping = {
    "killfeed": [(0.05, 0.26), (0.73, -0.042)],
    "minimap": [(0.0417, 0.278), (0.026, 0.15625)],
    "playercount": [(0.02, 0.1), (0.92, 0.98)],
    "round": [(0.26, 0.35), (0.02, 0.12)],
    "clock": [(0.25, 0.37), (0.04, 0.16)],
    "primary": [(0.95, 0.995), (0.79, 0.87)],
    "secondary": [(0.93, 0.995), (0.88, .98)]
}


def _crop(frame, coords=None, dim=None [1080, 1920]):
    """
    Return a cropped frame based on the UI Element on screen

    Parameters
    ----------
    key: string
        UI Element. Acceptable keys are ['killfeed', 'minimap', 'playercount', 'round', 'clock', 'primary', 'secondary']
    frame: np.array
        Numpy Array of the image to be cropped
    dim: list
        Dimensions of the image.
    coords: np.array of shape (2,2)
        Override crop for to 
    """
    if not dim:
        dim = frame.shape
    if coords.shape != (2, 2) or len(dim) != 2:
        raise ValueError(f'Improper Parameter Shape')
    bounds = [
        slice(*b) for b in (dim * np.array(coords)).T.astype(int)
    ]
    return frame[bounds]


def killfeed(frame, dim=None):
    return _crop(frame, ui_mapping["killfeed"], dim=dim)
 
def minimap(frame, dim=None):
    return _crop(frame, ui_mapping["minimap"], dim=dim)
 
def playercount(frame, dim=None):
    return _crop(frame, ui_mapping["playercount"], dim=dim)
 
def round(frame, dim=None):
    return _crop(frame, ui_mapping["round"], dim=dim)
 
def clock(frame, dim=None):
    return _crop(frame, ui_mapping["clock"], dim=dim)
 
def primary(frame, dim=None):
    return _crop(frame, ui_mapping["primary"], dim=dim)
 
def secondary(frame, dim=None):
    return _crop(frame, ui_mapping["secondary"], dim=dim)

def frame(frame, dim=None):
    return {
        k: _crop(frame, v,dim)
        for k,v in ui_mapping.items()
    }

