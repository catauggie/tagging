import sys
import os
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QPushButton, QSplitter, QTextEdit, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

import xml.etree.ElementTree as ET

class PDFXMLViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF and XML Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and layout for the main window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a splitter to divide the window into left and right sections
        splitter = QSplitter(Qt.Horizontal)

        # Create a PDF viewer widget on the left side within a scroll area
        pdf_scroll_area = QScrollArea()
        self.pdf_viewer = QWidget()
        self.pdf_viewer.setLayout(QVBoxLayout())  # Create a layout for the PDF viewer
        pdf_scroll_area.setWidget(self.pdf_viewer)
        pdf_scroll_area.setWidgetResizable(True)  # Make the scroll area resizable
        splitter.addWidget(pdf_scroll_area)

        # Create an XML viewer widget on the right side
        self.xml_viewer = QTextEdit(self)
        splitter.addWidget(self.xml_viewer)

        layout.addWidget(splitter)

        # Create a button to open the folder containing PDF and XML files
        open_button = QPushButton("Open Folder", self)
        open_button.clicked.connect(self.openFolder)
        layout.addWidget(open_button)

    def openFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing PDF and XML Files")

        if folder_path:
            pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]
            xml_files = [file for file in os.listdir(folder_path) if file.endswith(".xml")]

            if pdf_files and xml_files:
                # Display the first PDF and XML file in the folder
                pdf_file_path = os.path.join(folder_path, pdf_files[0])
                xml_file_path = os.path.join(folder_path, xml_files[0])

                self.displayPDF(pdf_file_path)
                self.displayXML(xml_file_path)

    def displayPDF(self, pdf_path):
        # Clear any existing widgets in the PDF viewer area
        pdf_layout = self.pdf_viewer.layout()
        while pdf_layout.count():
            item = pdf_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Use PyMuPDF to render and display all pages of the PDF file within the scrollable area
        pdf_document = fitz.open(pdf_path)

        for page_num in range(len(pdf_document)):
            pdf_page = pdf_document.load_page(page_num)
            pixmap = pdf_page.get_pixmap()
            qt_pixmap = QPixmap.fromImage(QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888))
            label = QLabel(self)
            label.setPixmap(qt_pixmap)
            pdf_layout.addWidget(label)

    def displayXML(self, xml_path):
        # Read and display the content of the XML file
        with open(xml_path, 'r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()
            self.xml_viewer.setPlainText(xml_content)


def main():
    app = QApplication(sys.argv)
    viewer = PDFXMLViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
