from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget, QSizePolicy
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

import cv2

from gui.modules.module import Module
from gui.event_nodes.subscriber import GUIEventSubscriber

from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class VideoWidget(QLabel):
    """A single video stream widget."""

    update_big_video_signal = pyqtSignal(QWidget)
    handle_frame_signal = pyqtSignal(Image)

    def __init__(self, index: int, topic: str):
        super().__init__()

        self.index: int = index

        # For debugging, display row number in each VideoWidget
        self.setText(str(index))

        self.cv_bridge: CvBridge = CvBridge()

        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Expanding)

        self.handle_frame_signal.connect(self.handle_frame)
        self.camera_subscriber: GUIEventSubscriber = GUIEventSubscriber(
            Image, topic, self.handle_frame_signal)
        self.camera_subscriber.spin_async()

    def mousePressEvent(self, event):
        """Swap this video with the big video on click."""
        if self.index != 0:
            self.update_big_video_signal.emit(self)

    @pyqtSlot(Image)
    def handle_frame(self, frame: Image):
        cv_image = self.cv_bridge.imgmsg_to_cv2(
            frame, desired_encoding='passthrough')

        # TODO: dynamic image scaling based on Qt element size
        qt_image: QImage = self.convert_cv_qt(
            cv_image,
            self.frameGeometry().width(),
            self.frameGeometry().height()
        )

        # self.setPixmap(qt_image.scaled(
        #     self.frameGeometry().width(),
        #     self.frameGeometry().height(),
        #     Qt.KeepAspectRatio))

        self.setPixmap(QPixmap.fromImage(qt_image))

    def convert_cv_qt(self, cv_img, width=None, height=None) -> QImage:
        """Convert from an opencv image to QPixmap."""

        # Color image
        if len(cv_img.shape) == 3:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = cv_img.shape
            bytes_per_line = ch * w

            img_format = QImage.Format_RGB888

        # Grayscale image
        elif len(cv_img.shape) == 2:
            h, w = cv_img.shape
            bytes_per_line = w

            img_format = QImage.Format_Grayscale8

        qt_image = QImage(cv_img.data, w, h, bytes_per_line, img_format)

        if width is not None:
            qt_image = qt_image.scaled(width, height, Qt.KeepAspectRatio)

        self.qt_image = qt_image

        return qt_image


class VideoArea(Module):
    """Container widget handling all video streams."""

    # First entry here will start as the big video
    CAMERA_TOPICS = ['/image/image_raw', '/bottom_cam/image_raw', '/front_cam/image_raw']
    CAMERA_COORDS = [(0,0), (0,1), (1,0)]

    def __init__(self):
        super().__init__()

        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)
        self.grid_layout.setRowStretch(0, 4)
        self.grid_layout.setRowStretch(1, 4)

        # MAGIC VALUE WARNING: i=0 represents the big video
        self.video_widgets: list[VideoWidget] = []
        for i, topic in enumerate(self.CAMERA_TOPICS):
            video: VideoWidget = VideoWidget(i, topic)
            self.video_widgets.append(video)

            self.grid_layout.addWidget(video, self.CAMERA_COORDS[i][0], self.CAMERA_COORDS[i][1], 1, 3)

            # video.update_big_video_signal.connect(self.set_as_big_video)

            # if i == 0:
            #     self.grid_layout.addWidget(video, 0, 0, 1, 3)
            # else:
            #     self.grid_layout.addWidget(video, 1, i - 1, 1, 1)

    def kill_module(self):
        for video_widget in self.video_widgets:
            video_widget.camera_subscriber.kill_executor()

    @pyqtSlot(QWidget)
    def set_as_big_video(self, target_widget: VideoWidget):
        """Swap target VideoWidget with big VideoWidget."""
        big_widget: QWidget = self.grid_layout.itemAtPosition(
            0, 0).widget()

        self.grid_layout.removeWidget(target_widget)
        self.grid_layout.removeWidget(big_widget)

        big_widget.index = target_widget.index
        target_widget.index = 0  # 0 still represents the big video

        small_frame_geometry = target_widget.frameGeometry()

        self.grid_layout.addWidget(target_widget, 0, 0, 1, 3)
        self.grid_layout.addWidget(big_widget, 1, big_widget.index - 1, 1, 1)

        target_widget.setPixmap(QPixmap.fromImage(target_widget.qt_image.scaled(
            big_widget.frameGeometry().width(),
            big_widget.frameGeometry().height())))

        big_widget.setPixmap(QPixmap.fromImage(big_widget.qt_image.scaled(
            small_frame_geometry.width(),
            small_frame_geometry.height())))
