from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt6.QtCore import Qt, QPoint


class AvatarWidget(QWidget):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name[0].upper() if name != None and name != "" else "U"
        self.setFixedSize(36, 36)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        radius = 18
        circle_color = QColor("#3498db")
        text_color = QColor("white")
        center = QPoint(self.width() // 2, self.height() // 2)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(circle_color))
        painter.drawEllipse(center, radius, radius)

        painter.setPen(QPen(text_color))
        
        font = QFont("Arial", 16)
        font.setBold(True)
        painter.setFont(font)

        text_rect = self.rect()
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.name)
        painter.end()