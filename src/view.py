from PySide2 import QtWidgets, QtCore, QtGui
from .ui_view import Ui_View
import os

from opencmiss.zinc.scenecoordinatesystem import SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT

class View(QtWidgets.QWidget):
    def __init__(self, scene, parent=None):
        super(View, self).__init__(parent)
        self._airwayFilenames = ['', '']
        self._surfaceFilenames = ['', '']
        self._outputFilenames = ['', '']
        self._path = '.'
        self._info = ''
        self._airwayCallback = None
        self._surfaceCallback = None
        self._generateCallback = None
        self._saveCallback = None

        self._ui = Ui_View()
        self._ui.setupUi(self)

        self._scene = scene
        self._ui.sceneviewer_widget.setContext(scene.getContext())
        self._makeConnections()

    def setInfo(self, info):
        self._info = info
    
    def _infoClicked(self):
        QtWidgets.QMessageBox.information(self, 'Information', self._info)

    def airwayCallback(self, cb):
        self._airwayCallback = cb

    def surfaceCallback(self, cb):
        self._surfaceCallback = cb

    def generateCallback(self, cb):
        self._generateCallback = cb

    def saveCallback(self, cb):
        self._saveCallback = cb

    def _makeConnections(self):
        self._ui.sceneviewer_widget.graphicsInitialized.connect(self._graphicsUpdate)
        self._ui.generate_pushButton.clicked.connect(self._generateClicked)
        self._ui.save_pushButton.clicked.connect(self._saveClicked)
        self._ui.airwayIpnode_pushButton.clicked.connect(self._airwayIpnodeClicked)
        self._ui.airwayIpelem_pushButton.clicked.connect(self._airwayIpelemClicked)
        self._ui.loadAirway_pushButton.clicked.connect(self._loadAirwayClicked)
        self._ui.surfaceIpnode_pushButton.clicked.connect(self._surfaceIpnodeClicked)
        self._ui.surfaceIpelem_pushButton.clicked.connect(self._surfaceIpelemClicked)
        self._ui.loadSurface_pushButton.clicked.connect(self._loadSurfaceClicked)
        self._ui.outputExnode_pushButton.clicked.connect(self._outputExnodeClicked)
        self._ui.outputExelem_pushButton.clicked.connect(self._outputExelemClicked)

        self._ui.info_pushButton.clicked.connect(self._infoClicked)
        self._ui.info_pushButton.setIcon(QtGui.QIcon.fromTheme('dialog-information'))
        self._ui.info_pushButton.setText('')

    def _graphicsUpdate(self):
        sceneviewer = self._ui.sceneviewer_widget.getSceneviewer()
        if sceneviewer is not None:
            self._ui.sceneviewer_widget.setScene(self._scene.getScene())
            sceneviewer.setLookatParametersNonSkew([1.9, -4.5, 2.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
            sceneviewer.setTransparencyMode(sceneviewer.TRANSPARENCY_MODE_SLOW)
            sceneviewer.viewAll()

    def setAirways(self, ipnode, ipelem):
        self._ui.airwayIpnode_lineEdit.setText(os.path.relpath(ipnode, os.getcwd()))
        self._ui.airwayIpelem_lineEdit.setText(os.path.relpath(ipelem, os.getcwd()))
        self._airwayFilenames[0] = str(ipnode)
        self._airwayFilenames[1] = str(ipelem)
        self._loadAirwayClicked()
    
    def _airwayIpnodeClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open airway ipnode file', dir=self._path, filter='*.ipnode')
        if filename:
            self._ui.airwayIpnode_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._airwayFilenames[0] = str(filename)
            self._path = os.path.dirname(filename)

    def _airwayIpelemClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open airway ipelem file', dir=self._path, filter='*.ipelem')
        if filename:
            self._ui.airwayIpelem_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._airwayFilenames[1] = str(filename)
            self._path = os.path.dirname(filename)

    def _loadAirwayClicked(self):
        if self._airwayCallback and self._airwayFilenames[0] and self._airwayFilenames[1]:
            self._airwayCallback(self._airwayFilenames[0], self._airwayFilenames[1])

    def setSurfaces(self, ipnode, ipelem):
        self._ui.surfaceIpnode_lineEdit.setText(os.path.relpath(ipnode, os.getcwd()))
        self._ui.surfaceIpelem_lineEdit.setText(os.path.relpath(ipelem, os.getcwd()))
        self._surfaceFilenames[0] = str(ipnode)
        self._surfaceFilenames[1] = str(ipelem)
        self._loadSurfaceClicked()
    
    def _surfaceIpnodeClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open surface ipnode file', dir=self._path, filter='*.ipnode')
        if filename:
            self._ui.surfaceIpnode_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._surfaceFilenames[0] = str(filename)
            self._path = os.path.dirname(filename)

    def _surfaceIpelemClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open surface ipelem file', dir=self._path, filter='*.ipelem')
        if filename:
            self._ui.surfaceIpelem_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._surfaceFilenames[1] = str(filename)
            self._path = os.path.dirname(filename)

    def _loadSurfaceClicked(self):
        if self._surfaceCallback and self._surfaceFilenames[0] and self._surfaceFilenames[1]:
            self._surfaceCallback(self._surfaceFilenames[0], self._surfaceFilenames[1])

    def setOutputs(self, exnode, exelem):
        self._ui.outputExnode_lineEdit.setText(os.path.relpath(exnode, os.getcwd()))
        self._ui.outputExelem_lineEdit.setText(os.path.relpath(exelem, os.getcwd()))
        self._outputFilenames[0] = str(exnode)
        self._outputFilenames[1] = str(exelem)
    
    def _outputExnodeClicked(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption='Save output exnode file', dir=self._path, filter='*.exnode')
        if filename:
            self._ui.outputExnode_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._outputFilenames[0] = str(filename)
            self._path = os.path.dirname(filename)

    def _outputExelemClicked(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption='Save output exelem file', dir=self._path, filter='*.exelem')
        if filename:
            self._ui.outputExelem_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._outputFilenames[1] = str(filename)
            self._path = os.path.dirname(filename)

    def _generateClicked(self):
        options = {
            "gridSize": self._ui.gridSize_doubleSpinBox.value(),
            "startNode": self._ui.startNode_spinBox.value(),
            "angleMax": self._ui.angleMax_doubleSpinBox.value(),
            "angleMin": self._ui.angleMin_doubleSpinBox.value(),
            "branchFraction": self._ui.branchFraction_doubleSpinBox.value(),
            "lengthLimit": self._ui.lengthLimit_doubleSpinBox.value(),
            "shortestLength": self._ui.shortestLength_doubleSpinBox.value(),
            "rotationLimit": self._ui.rotationLimit_doubleSpinBox.value(),
            "reset": self._ui.reset_checkBox.isChecked(),
        }

        if self._generateCallback:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self._generateCallback(self._airwayFilenames[0], self._airwayFilenames[1], self._surfaceFilenames[0], self._surfaceFilenames[1], options)
            QtWidgets.QApplication.restoreOverrideCursor()
        
    def _saveClicked(self):
        if self._saveCallback:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self._saveCallback(self._outputFilenames[0], self._outputFilenames[1])
            QtWidgets.QApplication.restoreOverrideCursor()
