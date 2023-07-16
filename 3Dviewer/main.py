from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import pyqtgraph as pg
from PyQt5.uic import loadUi
import SimpleITK as sitk
from plots import Plots
import sys
import numpy as np

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('main.ui', self)
        self.plots = Plots(self)
        self.actionOpen.triggered.connect(self.browse_files)

        pg.setConfigOption('imageAxisOrder', 'row-major')

    def browse_files(self):
        self.dir_name = "out.mhd"
        self.volume_array = self.importer(self.dir_name)

        self.center_lines(self.volume_array)
        arr = np.flipud(self.volume_array[35, :, :])
        arr = np.rot90(arr, 3)
        self.ax_image.setImage(arr, autoLevels = True)
        arr2 = np.flipud(self.volume_array[:, 128, :])
        arr2 = np.rot90(arr2, 3)
        self.cor_image.setImage(arr2, autoLevels = True)
        arr3 = np.flipud(self.volume_array[:, :, 128])
        arr3 = np.rot90(arr3, 3)
        self.sag_image.setImage(arr3, autoLevels = True)

        self.ax_vline.sigPositionChanged.connect(lambda: self.update_image(self.volume_array,"a", self.spinBox.value()))
        self.ax_hline.sigPositionChanged.connect(lambda: self.update_image(self.volume_array,"a", self.spinBox.value()))
        self.ax_oline.sigPositionChanged.connect(lambda: self.update_image(self.volume_array,"a", self.spinBox.value()))

        self.sag_vline.sigPositionChanged.connect(lambda: self.update_image(self.volume_array,"s"))
        self.sag_hline.sigPositionChanged.connect(lambda: self.update_image(self.volume_array,"s"))

        self.cor_vline.sigPositionChanged.connect(lambda: self.update_image(self.volume_array,"c"))
        self.cor_hline.sigPositionChanged.connect(lambda: self.update_image(self.volume_array,"c"))

        self.ob_hline.sigPositionChanged.connect(lambda: self.update_image(self.volume_array,"o"))
        self.spinBox.valueChanged.connect(lambda: self.update_image(self.volume_array,"a", self.spinBox.value()))

    def importer(self, path):
        # reader = sitk.ImageSeriesReader()
        # dicom_names = reader.GetGDCMSeriesFileNames(path)
        # reader.SetFileNames(dicom_names)
        # image = reader.Execute()
        itkimage = sitk.ReadImage(path)
        image_array = sitk.GetArrayFromImage(itkimage)
        return image_array

    def center_lines(self, arr):
        self.ax_vline.setValue(arr.shape[1] // 2)
        self.ax_hline.setValue(arr.shape[2] // 2)
        self.ax_oline.setValue((arr.shape[1] // 2, arr.shape[2] // 2))

        self.sag_vline.setValue(arr.shape[1] // 2)
        self.sag_hline.setValue(arr.shape[0] // 2)

        self.cor_vline.setValue(arr.shape[2] // 2)
        self.cor_hline.setValue(arr.shape[0] // 2)

    def update_image(self, arr = None, axes = None, angle = 45):
        if arr is None:
            print("No array passed to update_image")
            return
        if axes == 'a':
            self.cor_vline.setValue(self.ax_vline.value())
            self.sag_vline.setValue(self.ax_hline.value())
            view1 = np.flipud(arr[:, :, int(self.ax_vline.value())])
            view1 = np.rot90(view1, 3)
            view2 = np.flipud(arr[:, int(self.ax_hline.value()), :])
            view2 = np.rot90(view2, 3)
            self.sag_image.setImage(view1)
            self.cor_image.setImage(view2)
            self.ax_oline.setAngle(angle)
            view = np.flipud(arr)
            view = np.rot90(view, 3)
            if angle != 0 and angle != 180:
                self.ob_image.setImage(self.get_ob_slice(view, angle, self.ax_oline.value()))
        
        elif axes == 'c':
            self.ax_vline.setValue(self.cor_vline.value())
            self.sag_hline.setValue(self.cor_hline.value())
            self.ob_hline.setValue(self.cor_hline.value())
            view1 = np.flipud(arr[int(self.cor_hline.value()), :, :])
            view1 = np.rot90(view1, 3)
            view2 = np.flipud(arr[:, :, int(self.cor_vline.value())])
            view2 = np.rot90(view2, 3)
            self.ax_image.setImage(view1)
            self.sag_image.setImage(view2)
        
        elif axes == 's':
            self.ax_hline.setValue(self.sag_vline.value())
            self.cor_hline.setValue(self.sag_hline.value())
            self.ob_hline.setValue(self.sag_hline.value())
            view1 = np.flipud(arr[int(self.sag_hline.value()), :, :])
            view1 = np.rot90(view1, 3)
            view2 = np.flipud(arr[:, int(self.sag_vline.value()), :])
            view2 = np.rot90(view2, 3)
            self.ax_image.setImage(view1)
            self.cor_image.setImage(view2)

        elif axes == 'o':
            self.cor_hline.setValue(self.ob_hline.value())
            self.sag_hline.setValue(self.ob_hline.value())
            view1 = np.flipud(arr[int(self.ob_hline.value()), :, :])
            view1 = np.rot90(view1, 3)
            self.ax_image.setImage(view1)

    def get_ob_slice(self, arr, angle, point):
            angle = angle * np.pi / 180
            slope = np.tan(angle)

            if type(point) == list:
                y = point[1]
                z = point[0]
            elif angle - np.pi/2 < 0.01:
                y = 0
                z = point
            elif angle == np.pi:
                y = point
                z = 0
                
            y0 = y - slope * z
            z0 = z - y / slope
            zb = (arr.shape[1] - y0) / slope

            if zb >= arr.shape[2]:
                zb = arr.shape[2] - 1
            elif zb < 0:
                zb = 0
                
            if z0 >= arr.shape[2]:
                z0 = arr.shape[2] - 1
            elif z0 < 0:
                z0 = 0

            z_coords = np.linspace(int(z0), int(zb) - 1, arr.shape[2])
            y_coords = z_coords * slope + y0
            
            for i in range(len(y_coords)):
                y = int(round(y_coords[i]))
                if y < 0 or y>= arr.shape[1]:
                    y_coords[i] = 0

            z_coords = np.round(z_coords)

            plane = arr[:, y_coords.astype(int), z_coords.astype(int)]
            plane = np.squeeze(plane)
            
            return plane


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Main()
    widget.show()
    sys.exit(app.exec())