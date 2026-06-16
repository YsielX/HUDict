import signal
import sys

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
from PyQt6.QtGui import QIcon

from hudict.popup import Popup
from hudict.worker import LookupWorker


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    popup = Popup()
    worker = LookupWorker()
    worker.entries_ready.connect(popup.show_entries)
    worker.hide_requested.connect(popup.hide_popup)
    worker.start()

    tray = QSystemTrayIcon(QIcon())
    tray.setToolTip("HUDict")
    tray.show()

    def shutdown(*_):
        worker.stop()
        app.quit()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
