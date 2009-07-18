from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import ceil
from random import randrange
from util import left_most_bit
from fractals import Mandelbrot
from permutations import random_permutation,fract8_create

class ViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("PyMan"))
        self.resize(256, 256)

        self.instant = False
        self.fractal = Mandelbrot(50)
        self.offset = QPointF()
        self.scale = 5
        self.last_pos = QPointF()
        self.resize_pixmap()

    def resize_pixmap(self):
        self.pixmap = QPixmap(self.width(), self.height())
        self.pixmap.fill(QColor())

        self.buck_size_log = 4
        self.buck_size = 2 ** self.buck_size_log
        self.buck_size_sq = self.buck_size ** 2

        self.nr_buck = ceil(self.width()  / self.buck_size) * \
                       ceil(self.height() / self.buck_size)

        self.perm_x,self.perm_y = fract8_create()
        self.buck_perm = random_permutation(self.nr_buck)

        self.reset_pixels()

    def reset_pixels(self):
        self.buck_offs = [2 ** randrange(2*self.buck_size_log) for i in range(self.nr_buck)]
        self.buck_pix  = [0] * self.nr_buck
        self.nr_pixels = 0
        self.update()

    def update_pixels(self, n=1000):
        n = min(n, len(self.buck_perm) * self.buck_size_sq - self.nr_pixels)
        painter = QPainter(self.pixmap)
        center = QPointF(self.width() / 2, self.height() / 2)
        for i in range(n):
            buck = self.buck_perm[self.nr_pixels % len(self.buck_perm)]
            self.nr_pixels += 1

            (by,bx) = divmod(buck, ceil(self.width() / self.buck_size))
            (bx,by) = (bx*self.buck_size, by*self.buck_size)
            assert self.buck_pix[buck] < self.buck_size_sq
            pix = (self.buck_pix[buck] + self.buck_offs[buck]) % self.buck_size_sq
            (px,py) = (self.perm_x[pix] >> self.buck_size_log, self.perm_y[pix] >> self.buck_size_log)
            self.buck_pix[buck] += 1
            (x,y) = (bx+px,by+py)
            if x >= self.width() or y >= self.height():
                continue

            p = QPointF(x,y) - center
            p = self.offset + QPointF(p.x() / self.width(), p.y() / self.height()) * self.scale
            p = complex(p.x(), p.y())
            c = self.fractal(p)

            if not self.instant:
                painter.fillRect(QRect(x, y, 1, 1), c)
            else:
                # THIS IS STILL EXPERIMENTAL
                k = left_most_bit(self.buck_pix[buck])
                if self.buck_pix[buck] > (1 << k):
                    k += 1
                if k % 2:
                    k += 1
                k = k // 2 + k % 2
                l = self.buck_size_log - k
                (nx,ny) = (bx + ((px >> l) << l), by + ((py >> l) << l))
                painter.fillRect(QRect(nx, ny, 1 << l, 1 << l), c)
                
        return self.nr_pixels == len(self.buck_perm) * self.buck_size_sq

    def paintEvent(self, event):
        done = self.update_pixels()
        QPainter(self).drawPixmap(0, 0, self.pixmap)
        if not done:
            self.update()

    def resizeEvent(self, event):
        self.resize_pixmap()

    def wheelEvent(self, event):
        numDegrees = event.delta() / 8
        numSteps = numDegrees / 15.0
        self.scale *= pow(0.8, numSteps)
        self.reset_pixels()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.last_pos = QPointF(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            dxy = QPointF(event.pos()) - self.last_pos
            self.offset -= QPointF(dxy.x() / self.width(), dxy.y() / self.height()) * self.scale
            self.last_pos = QPointF(event.pos())
            self.reset_pixels()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            dxy = QPointF(event.pos()) - self.last_pos
            self.offset -= QPointF(dxy.x() / self.width(), dxy.y() / self.height()) * self.scale
            self.reset_pixels()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_I:
            self.instant = not self.instant
            self.reset_pixels()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = ViewerWidget()
    widget.show()
    sys.exit(app.exec_())
