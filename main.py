#!/usr/bin/env python3
from math import ceil
from random import randrange
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from fractals import Mandelbrot
from permutations import random_permutation, fract8_create
from util import left_most_bit


class ViewerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ViewerWidget, self).__init__(parent)
        self.setWindowTitle(self.tr("PyMan"))
        self.resize(720, 720)

        self.instant = True
        self.fractal = Mandelbrot(50)
        self.offset = QtCore.QPointF(-0.5, 0)
        self.scale = 5
        self.last_pos = QtCore.QPointF()
        self.resize_pixmap()

    def resize_pixmap(self):
        self.pixmap = QtGui.QPixmap(self.width(), self.height())
        self.pixmap.fill(QtGui.QColor())

        self.buck_size_log = 4
        self.buck_size = 2 ** self.buck_size_log
        self.buck_size_sq = self.buck_size ** 2

        self.nr_buck = int(ceil(self.width() / self.buck_size) *
                           ceil(self.height() / self.buck_size))
        self.perm_xy = [list(zip(*fract8_create())) for i in range(5)]
        self.reset_pixels()

    def reset_pixels(self):
        self.buck_pix = [0] * self.nr_buck
        self.buck_perm = random_permutation(self.nr_buck)
        self.nr_pixels = 0
        self.update()

    def update_pixels(self, n=1000):
        n = min(n, len(self.buck_perm) * self.buck_size_sq - self.nr_pixels)
        painter = QtGui.QPainter(self.pixmap)
        center = QtCore.QPointF(self.width() / 2, self.height() / 2)
        for i in range(n):
            buck = self.buck_perm[self.nr_pixels % len(self.buck_perm)]
            perm = self.buck_perm[buck] % 5
            self.nr_pixels += 1

            by, bx = divmod(buck, ceil(self.width() / self.buck_size))
            bx, by = (bx*self.buck_size, by*self.buck_size)
            px, py = self.perm_xy[perm][self.buck_pix[buck]]
            px, py = (px >> self.buck_size_log, py >> self.buck_size_log)
            self.buck_pix[buck] += 1
            x, y = (bx+px, by+py)

            p = QtCore.QPointF(x, y) - center
            p = self.offset + QtCore.QPointF(p.x() / self.width(), p.y() / self.height()) * self.scale
            p = complex(p.x(), p.y())
            c = self.fractal(p)

            if not self.instant:
                painter.fillRect(QtCore.QRect(x, y, 1, 1), c)
            else:
                k = left_most_bit(self.buck_pix[buck])
                if self.buck_pix[buck] > (1 << k):
                    k += 1
                k = k // 2 + k % 2
                l = self.buck_size_log - k
                nx, ny = (bx + ((px >> l) << l), by + ((py >> l) << l))
                painter.fillRect(QtCore.QRect(nx, ny, 1 << l, 1 << l), c)

        return self.nr_pixels == len(self.buck_perm) * self.buck_size_sq

    def paintEvent(self, event):
        done = self.update_pixels()
        QtGui.QPainter(self).drawPixmap(0, 0, self.pixmap)
        if not done:
            self.update()

    def resizeEvent(self, event):
        self.resize_pixmap()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.scale *= 1.0 + delta / 360.0
        self.reset_pixels()

    def mousePressEvent(self, event):
        self.last_pos = QtCore.QPointF(event.position())

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            dxy = QtCore.QPointF(event.position()) - self.last_pos
            self.offset -= QtCore.QPointF(dxy.x() / self.width(), dxy.y() / self.height()) * self.scale
            self.last_pos = QtCore.QPointF(event.position())
            self.reset_pixels()
        elif event.buttons() & QtCore.Qt.RightButton:
            dxy = QtCore.QPointF(event.position()) - self.last_pos
            self.scale *= pow(5, -(dxy.x() / self.width() + dxy.y() / self.height()))
            self.last_pos = QtCore.QPointF(event.position())
            self.reset_pixels()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            dxy = QtCore.QPointF(event.position()) - self.last_pos
            self.offset -= QtCore.QPointF(dxy.x() / self.width(), dxy.y() / self.height()) * self.scale
            self.reset_pixels()

    def keyPressEvent(self, event):
        key, mod = event.key(), event.modifiers()
        if key == QtCore.Qt.Key_Q and mod == QtCore.Qt.ControlModifier:
            self.close()
        elif key == QtCore.Qt.Key_I:
            self.instant = not self.instant
            self.reset_pixels()
        elif key == QtCore.Qt.Key_Left:
            self.offset -= QtCore.QPointF(0.1, 0.0) * self.scale
            self.reset_pixels()
        elif key == QtCore.Qt.Key_Right:
            self.offset -= QtCore.QPointF(-0.1, 0.0) * self.scale
            self.reset_pixels()
        elif key == QtCore.Qt.Key_Up:
            self.offset -= QtCore.QPointF(0.0, 0.1) * self.scale
            self.reset_pixels()
        elif key == QtCore.Qt.Key_Down:
            self.offset -= QtCore.QPointF(0.0, -0.1) * self.scale
            self.reset_pixels()
        elif key in [QtCore.Qt.Key_Equal, QtCore.Qt.Key_Plus]:
            self.scale *= 0.8
            self.reset_pixels()
        elif key in [QtCore.Qt.Key_Minus, QtCore.Qt.Key_Underscore]:
            self.scale /= 0.8
            self.reset_pixels()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = ViewerWidget()
    widget.show()
    sys.exit(app.exec())
