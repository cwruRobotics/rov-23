import re

from gui.event_nodes.event_node import GUIEventNode
from rclpy.publisher import MsgType


class GUIEventPublisher(GUIEventNode):
    """Publisher for sending messages from the GUI."""

    def __init__(self, msg_type: MsgType, topic: str):
        # Name this node with a sanitized version of the topic
        super().__init__(
            f'gui_event_publisher_{re.sub(r"[^a-zA-Z0-9_]", "_", topic)}')

        self.publisher = self.create_publisher(msg_type, topic, 10)

    def publish(self, msg: MsgType):
        """Send a message with the provided parameters."""
        self.publisher.publish(msg)
