<<<<<<< HEAD
def parse_killfeed(frame):
    return frame[150:250, 1450:-100]


def parse_minimap(frame):
    return frame[45:300, 50:300]


def parse_playercount(frame):
    return frame[55:75, 1760:1782]


def parse_round(frame):
    return frame[340:360, 50:200]


def parse_clock(frame):
    return frame[335:360, 200:300]
=======
def parse_killfeed(frame, dim=[1080, 1920]):
    return frame[int(0.05 * dim[0]):int(0.26 * dim[0]), int(0.73 * dim[1]):int(-0.042 * dim[1])]


def parse_minimap(frame, dim=[1080, 1920]):
    return frame[int(0.0417 * dim[0]):int(0.278 * dim[0]), int(0.026 * dim[1]):int(0.15625 * dim[1])]


def parse_playercount(frame, dim=[1080, 1920]):
    return frame[int(0.02 * dim[0]):int(0.1 * dim[0]),
                 int(0.92 * dim[1]):int(0.98 * dim[1])]


def parse_round(frame, dim=[1080, 1920]):
    return frame[int(0.26 * dim[0]):int(0.35 * dim[0]),
                 int(0.02 * dim[1]):int(0.12 * dim[1])]

def parse_clock(frame, dim=[1080, 1920]):
    return frame[int(0.25 * dim[0]):int(0.37 * dim[0]),
                 int(0.04 * dim[1]):int(0.16 * dim[1])]

def parse_primary(frame,dim=[1080, 1920]):
    return frame[int(0.95 * dim[0]):int(.995 * dim[0]), int(.79 * dim[1]):int(.87 * dim[1])]

def parse_secondary(frame,dim=[1080, 1920]):
	return frame[int(0.93 * dim[0]):int(.995 * dim[0]), int(.88* dim[1]):int(.98* dim[1])]


f=lambda a,b,c,d: show_img(frame[int(a*dim[0]):int(b*dim[0]),int(c*dim[1]):int(d*dim[1])])


>>>>>>> 73d6c86e6136a1f51dd1a14071094f57ae7578d3
