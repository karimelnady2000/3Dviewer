from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg

class Plots:
    penV = pg.mkPen(color='r', width=0.5,style=QtCore.Qt.DashLine)
    penH = pg.mkPen(color='g', width=0.5,style=QtCore.Qt.DashLine)
    penO = pg.mkPen(color='b', width=0.5,style=QtCore.Qt.DashLine)

    def __init__(self, main):
        self.main = main
        Plots.init_ax(self.main)
        Plots.init_sag(self.main)
        Plots.init_cor(self.main)
        Plots.init_ob(self.main)

    def init_ax(self):
        self.ax_image = pg.ImageItem()
        
        self.axial_box.setAspectLocked(True)
        self.axial_box.showAxes(False)
        self.axial_box.setMouseEnabled(x=False, y=False)
        self.axial_box.addItem(self.ax_image)

        self.ax_vline = pg.InfiniteLine(angle=90, movable=True, pen=Plots.penV, name='ax_vline')
        self.ax_hline = pg.InfiniteLine(angle=0, movable=True, pen=Plots.penH, name='ax_hline')
        self.ax_oline = pg.InfiniteLine(angle=135, movable=True, pen=Plots.penO, name='ax_oline')
        self.axial_box.addItem(self.ax_vline)
        self.axial_box.addItem(self.ax_hline)
        self.axial_box.addItem(self.ax_oline)

    def init_sag(self):
        self.sag_image = pg.ImageItem()

        self.sagittal_box.setAspectLocked(True)
        self.sagittal_box.showAxes(False)
        self.sagittal_box.setMouseEnabled(x=False, y=False)
        self.sagittal_box.addItem(self.sag_image)

        self.sag_vline = pg.InfiniteLine(angle=90, movable=True, pen=Plots.penV, name='sag_vline')
        self.sag_hline = pg.InfiniteLine(angle=0, movable=True, pen=Plots.penH, name='sag_hline')
        self.sagittal_box.addItem(self.sag_vline)
        self.sagittal_box.addItem(self.sag_hline)

    def init_cor(self):
        self.cor_image = pg.ImageItem()

        self.coronal_box.setAspectLocked(True)
        self.coronal_box.showAxes(False)
        self.coronal_box.setMouseEnabled(x=False, y=False)
        self.coronal_box.addItem(self.cor_image)

        self.cor_vline = pg.InfiniteLine(angle=90, movable=True, pen=Plots.penV, name='cor_vline')
        self.cor_hline = pg.InfiniteLine(angle=0, movable=True, pen=Plots.penH, name='cor_hline')
        self.coronal_box.addItem(self.cor_vline)
        self.coronal_box.addItem(self.cor_hline)

    def init_ob(self):
        self.ob_image = pg.ImageItem()
        self.oblique_box.setAspectLocked(True)
        self.oblique_box.showAxes(False)
        self.oblique_box.setMouseEnabled(x=False, y=False)
        self.oblique_box.addItem(self.ob_image)
        self.ob_hline = pg.InfiniteLine(angle=0, movable=True, pen=Plots.penV, name='ob_hline')
        self.oblique_box.addItem(self.ob_hline)