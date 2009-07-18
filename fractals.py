from PyQt4.QtGui import QColor

def wave_to_color(wave):
    (r,g,b) = (0, 0, 0)
    if wave >= 380 and wave <= 440:
        r = -1 * (wave - 440) / (440 - 380)
        b = 1
    elif wave >= 440 and wave <= 490:
        g = (wave - 440) / (490 - 440)
        b = 1
    elif wave >= 490 and wave <= 510:
        g = 1
        b = -1 * (wave - 510) / (510 - 490)
    elif wave >= 510 and wave <= 580:
        r = (wave - 510) / (580 - 510)
        g = 1
    elif wave >= 580 and wave <= 645:
        r = 1
        g = -1 * (wave - 645) / (645 - 580)
    elif wave >= 645 and wave <= 780:
        r = 1

    s = 1
    if wave < 420:
        s = 0.3 + 0.7 * (wave - 380) / (420 - 380)
    elif wave > 700:
        s = 0.3 + 0.7 * (780 - wave) / (780 - 700)

    return QColor(*map(lambda x: 255 * pow(x * s, 0.8), (r, g, b)))

class ColorMap:
    def __init__(self, size=512):
        self.__size = size
        self.__colormap = [wave_to_color(380.0 + (i * 400.0 / size)) for i in range(size)]

    def __getitem__(self, idx):
        if idx < 0 or idx >= self.__size:
            raise IndexError('index out of range')
        return self.__colormap[idx]

class Mandelbrot:
    def __init__(self, iterations=512):
        self.__iterations = iterations
        self.__colormap = ColorMap(iterations)

    def __call__(self, p0):
        p = p0
        for i in range(self.__iterations):
            p = p0 + p**2
            if abs(p) > 4.0:
                return self.__colormap[i]
        return QColor()
