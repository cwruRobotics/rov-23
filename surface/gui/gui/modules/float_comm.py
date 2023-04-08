
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QLabel, QWidget
from gui.event_nodes.publisher import GUIEventPublisher
from gui.event_nodes.subscriber import GUIEventSubscriber
from std_msgs.msg import String
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class FloatComm(QWidget):
    """Arm widget for sending Arm Commands."""

    handle_scheduler_response_signal: pyqtSignal = pyqtSignal(String)

    def __init__(self):
        super().__init__()

        layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(layout)

        submerge_button = QPushButton()
        extend_button = QPushButton()
        retract_button = QPushButton()

        submerge_button.setText("Submerge")
        extend_button.setText("Extend")
        retract_button.setText("Retract")

        submerge_button.setFixedSize(300, 200)
        extend_button.setFixedSize(300, 200)
        retract_button.setFixedSize(300, 200)

        submerge_button.clicked.connect(self.submerge_clicked)
        extend_button.clicked.connect(self.extend_clicked)
        retract_button.clicked.connect(self.retract_clicked)

        layout.addWidget(submerge_button)
        layout.addWidget(extend_button)
        layout.addWidget(retract_button)

        self.handle_scheduler_response_signal.connect(self.handle_text)

        self.label: QLabel = QLabel()
        self.label.setText('Waiting for radio...')
        layout.addWidget(self.label)

        self.transceiver_publisher: GUIEventPublisher = GUIEventPublisher(
            String,
            "transceiver_control"
        )

        self.transceiver_subscription: GUIEventSubscriber = GUIEventSubscriber(
            String,
            "transceiver_data",
            self.handle_scheduler_response_signal
        )

    @pyqtSlot(String)
    def handle_text(self, msg: String):
        self.label.setText(msg.data)

    def submerge_clicked(self):
        self.transceiver_publisher.publish("submerge")

    def extend_clicked(self):
        self.transceiver_publisher.publish("extend")

    def retract_clicked(self):
        self.transceiver_publisher.publish("retract")
