import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from img_loader import ImgLoader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.img_loader = None
        self.current_image_path = None
        self.image_index = 0

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.image_label = QLabel(self)
        self.load_button = QPushButton('Load Dataset', self)
        self.next_button = QPushButton('Next Image', self)
        self.prev_button = QPushButton('Previous Image', self)

        self.init_ui()

    def init_ui(self) -> None:
        """Инициализация пользовательского интерфейса."""
        self.setWindowTitle('Images')
        self.setGeometry(100, 100, 800, 600)

        self.setCentralWidget(self.central_widget)

        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.load_button.clicked.connect(self.load_dataset)
        self.layout.addWidget(self.load_button)

        self.next_button.clicked.connect(self.next_image)
        self.layout.addWidget(self.next_button)

        self.prev_button.clicked.connect(self.prev_image)
        self.layout.addWidget(self.prev_button)

    def load_dataset(self) -> None:
        """Загрузка датасета из CSV файла."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Annotation File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_name:
            if os.path.exists(file_name):
                self.img_loader = ImgLoader(file_name)
                self.image_index = 0
                self.current_image_path = self.img_loader.img_paths[self.image_index] if self.img_loader.img_paths else None
                self.display_image()
            else:
                QMessageBox.warning(self, "Error", "File not found!")

    def next_image(self) -> None:
        """Переход к следующему изображению."""
        if self.img_loader:
            self.image_index += 1
            if self.image_index < len(self.img_loader.img_paths):
                self.current_image_path = self.img_loader.img_paths[self.image_index]
            else:
                self.image_index -= 1
            self.display_image()

    def prev_image(self) -> None:
        """Переход к предыдущему изображению."""
        if self.img_loader:
            self.image_index -= 1
            if self.image_index >= 0:
                self.current_image_path = self.img_loader.img_paths[self.image_index]
            else:
                self.image_index += 1
            self.display_image()

    def display_image(self) -> None:
        """Отображение текущего изображения."""
        if self.current_image_path:
            pixmap = QPixmap(self.current_image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image_label.setText("No more images")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())