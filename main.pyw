from PyQt4.QtCore import *
from PyQt4.QtGui import *
from fractals import Mandelbrot
from permutations import random_permutation

class ViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("PyMan"))
        self.resize(256, 256)

        self.fractal = Mandelbrot(50)
        self.offset = QPointF()
        self.scale = 5
        self.last_pos = QPointF()
        self.resize_pixmap()
        self.reset_pixels()

    def resize_pixmap(self):
        self.perm = random_permutation(self.width() * self.height())
        self.pixmap = QPixmap(self.width(), self.height())
        self.pixmap.fill(QColor())

    def reset_pixels(self):
        self.nr_pixels = 0
        self.update()

    def update_pixels(self, n=1000):
        n = min(n, self.width() * self.height() - self.nr_pixels)
        painter = QPainter(self.pixmap)
        center = QPointF(self.width() / 2, self.height() / 2)
        for i in range(n):
            (y,x) = divmod(self.perm[self.nr_pixels], self.width())
            p = QPointF(x,y) - center
            p = self.offset + QPointF(p.x() / self.width(), p.y() / self.height()) * self.scale
            p = complex(p.x(), p.y())
            c = self.fractal(p)
            self.nr_pixels += 1
            painter.fillRect(QRect(x, y, 1, 1), c)

    def paintEvent(self, event):
        self.update_pixels()
        QPainter(self).drawPixmap(0, 0, self.pixmap)
        if self.nr_pixels != self.width() * self.height():
            self.update()

    def resizeEvent(self, event):
        self.resize_pixmap()
        self.reset_pixels()

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

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = ViewerWidget()
    widget.show()
    sys.exit(app.exec_())
