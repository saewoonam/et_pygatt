from PyQt5.QtBluetooth import QLowEnergyController,\
    QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo
from PyQt5.QtCore import pyqtSlot, QThread, QCoreApplication, QObject,\
    pyqtSignal
import sys

class BTLEWorker(QObject):    
    def __init__(self, app:QCoreApplication=None, parent:QObject=None, *args, \
**kwargs):      self.app = app
            
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent
        self.le_controller = QLowEnergyController
                        
        super(BTLEWorker, self).__init__(parent=parent, *args, **kwargs)
                    
    def run(self):
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent()
                                
        self.discovery_agent.deviceDiscovered.connect(self.onDeviceDiscovered)
        self.discovery_agent.finished.connect(self.onDeviceDiscoveryFinished)
        self.discovery_agent.error.connect(self.onDeviceDiscoveryError)
        self.discovery_agent.setLowEnergyDiscoveryTimeout(1000)
        self.discovery_agent.start()
    
        self.enterLoop()
                            
    def enterLoop(self):
        th = self.thread()
        th.exec_()
        
    def exitLoop(self):
        th = self.thread()
        th.exit()
     
    #       
    # Slots for QDeviceDiscoveryAgent
    #                
    @pyqtSlot(QBluetoothDeviceInfo)
    def onDeviceDiscovered(self, devinfo: QBluetoothDeviceInfo):
        address = devinfo.address() #: :type address: QBluetoothAddress
        
        if devinfo.coreConfigurations() & \
                QBluetoothDeviceInfo.LowEnergyCoreConfiguration:
            print("Last device discovered", devinfo.name(), address.toString())
            
    @pyqtSlot()
    def onDeviceDiscoveryFinished(self):
        print("Discovery finished")
        
        self.exitLoop()
    
    @pyqtSlot(QBluetoothDeviceDiscoveryAgent.Error)
    def onDeviceDiscoveryError(self, error: QBluetoothDeviceDiscoveryAgent.Error):
        print("Bluetooth error", error)
        
        self.exitLoop()
    

class Controller(QObject):
    operate = pyqtSignal()
    
    def __init__(self, app=None, parent=None, *args, **kwargs):
        """
        @type app: QApplication
        @type parent: QObject
        """
        super(Controller, self).__init__(parent=parent, *args, **kwargs)
                
        self.app = app
        
        self.worker = BTLEWorker()
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        
        self.worker_thread.finished.connect(self.quit)
        self.operate.connect(self.worker.run)
                
        self.worker_thread.start()
                
    @pyqtSlot()
    def quit(self):
        """
        @rtype int
        """
        self.app.exit()
        
                
if __name__ == '__main__':    
    qapp = QCoreApplication(sys.argv)
    
    c = Controller(qapp)
    c.operate.emit()
    
    sys.exit(qapp.exec_())
------------------------ end of code that works ------------------------

------------------------ code that DOENST work ------------------------
from PyQt5.QtBluetooth import QLowEnergyController,\
    QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo
from PyQt5.QtCore import pyqtSlot, QThread, QCoreApplication, QObject
import sys


class BTLEWorker(QThread):    
    def __init__(self, app:QCoreApplication=None, parent:QObject=None, *args, \
**kwargs):      self.app = app
            
        self.discovered_devices = list()
        
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent
        self.le_controller = QLowEnergyController
                        
        super(BTLEWorker, self).__init__(parent=parent, *args, **kwargs)
                
    def run(self):
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent()
                                
        self.discovery_agent.deviceDiscovered.connect(self.onDeviceDiscovered) #THIS \
                FAILES
        self.discovery_agent.finished.connect(self.onDeviceDiscoveryFinished)
        self.discovery_agent.error.connect(self.onDeviceDiscoveryError)
        self.discovery_agent.setLowEnergyDiscoveryTimeout(1000)
        self.discovery_agent.start()
    
        self.enterLoop()
        
        self.app.exit()
                            
    def enterLoop(self):
        self.exec_()
        
    def exitLoop(self):
        self.exit()
     
    #       
    # Slots for QDeviceDiscoveryAgent
    #                
    @pyqtSlot(QBluetoothDeviceInfo)
    def onDeviceDiscovered(self, devinfo: QBluetoothDeviceInfo):
        address = devinfo.address() #: :type address: QBluetoothAddress
        
        if devinfo.coreConfigurations() & \
QBluetoothDeviceInfo.LowEnergyCoreConfiguration:  \
                self.discovered_devices.append(devinfo)
            print("Last device discovered", devinfo.name(), address.toString())
            
    @pyqtSlot()
    def onDeviceDiscoveryFinished(self):
        print("Discovery finished")
        
        self.exitLoop()
    
    @pyqtSlot(QBluetoothDeviceDiscoveryAgent.Error)
    def onDeviceDiscoveryError(self, error: QBluetoothDeviceDiscoveryAgent.Error):
        print("Bluetooth error", error)
        
        self.exitLoop()    
    
                
if __name__ == '__main__':    
    qapp = QCoreApplication(sys.argv)
    
    c = BTLEWorker(qapp)
    c.start()
    
    sys.exit(qapp.exec_())        
------------------------ end of code that DOENST work ------------------------


