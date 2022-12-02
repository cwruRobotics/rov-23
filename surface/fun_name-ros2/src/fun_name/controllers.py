import os

import rclpy
from ament_index_python.packages import get_package_share_directory

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget

package_share_dir = get_package_share_directory('fun_name')

class ControllersWidget(QWidget):
    namespace = ""

    stopping = False

    confirm_unkill = None

    def __init__(self, node: 'rclpy.Node'):
        super(ControllersWidget, self).__init__()
        self._node: 'rclpy.Node' = node
    
        # Load UI
        ui_file = os.path.join(package_share_dir, 'resource', 'ControllersPlugin.ui')
        loadUi(ui_file, self)
        self.setObjectName('ControllersPluginUi')

    def shutdown_plugin(self):
        self.stopping = True

        if self.confirm_unkill is not None:
            self.confirm_unkill.destroy(destroyWindow=True)
            self.confirm_unkill = None

class ControllersPlugin(Plugin):

    def __init__(self, context):
        super(ControllersPlugin, self).__init__(context)
        self._node = context.node

        # Give QObjects reasonable names
        self.setObjectName('ControllersPlugin')

        self._widget = ControllersWidget(self._node)
        
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)
    
    def shutdown_plugin(self):
        self._widget.shutdown_plugin()