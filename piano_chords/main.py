import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from pages.settings_page import SettingsPage
from pages.practice_page import PracticePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Piano Trainer")
        self.resize(800, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize pages
        self.settings_page = SettingsPage(self)
        self.practice_page = PracticePage(self)

        # Add pages to stacked widget
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.practice_page)

        # Show settings page first
        self.stack.setCurrentWidget(self.settings_page)

    def start_practice(self, selected_notes, chord_types, interval):
        """
        Called by SettingsPage when 'Start Practice' is clicked
        """
        self.practice_page.setup(selected_notes, chord_types, interval)
        self.stack.setCurrentWidget(self.practice_page)

    def back_to_settings(self):
        self.stack.setCurrentWidget(self.settings_page)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
