from PyQt5.QtWidgets import QGridLayout


from gui.modules.task_selector import TaskSelector
from gui.modules.logger import Logger
from gui.modules.float_comm import FloatComm
from gui.app import App


class OperatorApp(App):
    def __init__(self):
        super().__init__('operator_gui_node')

        self.setWindowTitle('Operator GUI - CWRUbotix ROV 2023')

        layout: QGridLayout = QGridLayout()
        self.setLayout(layout)

        self.task_selector: TaskSelector = TaskSelector()
        layout.addWidget(self.task_selector, 0, 1)

        self.logger: Logger = Logger()
        layout.addWidget(self.logger, 0, 2)

        self.float_comm: FloatComm = FloatComm()
        layout.addWidget(self.float_comm, 0, 0)


def run_gui_operator():
    OperatorApp().run_gui()
