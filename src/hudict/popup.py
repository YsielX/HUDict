from PyQt6.QtCore import QPoint, Qt, pyqtSlot
from PyQt6.QtGui import QColor, QCursor, QFont
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QVBoxLayout, QWidget

from hudict.config import config


class Popup(QWidget):
    def __init__(self):
        super().__init__()
        self.is_visible = False
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame()
        layout.addWidget(self.frame)
        self.content = QVBoxLayout(self.frame)
        self.content.setContentsMargins(10, 8, 10, 8)

        self.label = QLabel()
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setWordWrap(True)
        self.content.addWidget(self.label)

        self.apply_style()
        self.hide()

    def apply_style(self):
        bg = QColor(config.color_background)
        self.frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba({bg.red()}, {bg.green()}, {bg.blue()}, {config.background_opacity});
                color: {config.color_foreground};
                border-radius: 8px;
                border: 1px solid #555;
            }}
            QLabel {{
                background: transparent;
                border: none;
                font-family: "{config.font_family}";
            }}
        """)
        self.label.setFont(QFont(config.font_family))

    @pyqtSlot(object)
    def show_entries(self, entries):
        if not entries:
            self.hide_popup()
            return
        self.label.setText(self.render_entries(entries))
        self.label.adjustSize()
        self.adjustSize()
        self.move_near_cursor()
        self.show()
        self.raise_()
        self.is_visible = True

    @pyqtSlot()
    def hide_popup(self):
        if self.is_visible:
            self.hide()
            self.is_visible = False

    def render_entries(self, entries):
        parts = []
        for entry in entries[:3]:
            header = f'<span style="font-size:{config.font_size_header}px; color:{config.color_word};">{entry.word}</span>'
            if entry.phonetic:
                header += f' <span style="font-size:{config.font_size_header - 2}px; color:{config.color_reading};">[{entry.phonetic}]</span>'
            gloss = "; ".join(entry.glosses[:2])
            parts.append(f'{header}<br><span style="font-size:{config.font_size_definition}px;">{gloss}</span>')
        return '<hr style="border:none;height:1px;">'.join(parts)

    def move_near_cursor(self):
        cursor = QCursor.pos()
        screen = QApplication.screenAt(cursor) or QApplication.primaryScreen()
        geo = screen.geometry()
        offset = 16
        size = self.sizeHint()
        x = cursor.x() + offset
        y = cursor.y() + offset
        if x + size.width() > geo.right():
            x = cursor.x() - size.width() - offset
        if y + size.height() > geo.bottom():
            y = cursor.y() - size.height() - offset
        x = max(geo.left(), min(x, geo.right() - size.width()))
        y = max(geo.top(), min(y, geo.bottom() - size.height()))
        self.move(QPoint(int(x), int(y)))
