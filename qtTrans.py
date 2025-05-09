import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QLineEdit

class JsonToTxtConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON to TXT Converter")
        self.layout = QVBoxLayout()

        self.label_folder = QLabel("Select a folder containing JSON files to convert."
                                   "选择要转换的JSON文件夹。")
        self.layout.addWidget(self.label_folder)

        self.button_browse = QPushButton("Browse"
                                         "浏览")
        self.button_browse.clicked.connect(self.browse_folder)
        self.layout.addWidget(self.button_browse)

        self.label_output_folder = QLabel("Select output folder for TXT files:"
                                         "选择保存TXT文件的输出文件夹")
        self.layout.addWidget(self.label_output_folder)

        self.button_output_folder = QPushButton("Select Output Folder"
                                         "选择输出文件夹")
        self.button_output_folder.clicked.connect(self.select_output_folder)
        self.layout.addWidget(self.button_output_folder)

        self.label_class = QLabel("Enter class label:"
                                  "输入分类标签")
        self.layout.addWidget(self.label_class)

        self.input_class = QLineEdit()
        self.layout.addWidget(self.input_class)

        self.label_width = QLabel("Enter image width:"
                                  "输入图像宽度")
        self.layout.addWidget(self.label_width)

        self.input_width = QLineEdit()
        self.layout.addWidget(self.input_width)

        self.label_height = QLabel("Enter image height:"
                                   "输入图像高度")
        self.layout.addWidget(self.label_height)

        self.input_height = QLineEdit()
        self.layout.addWidget(self.input_height)

        self.button_convert = QPushButton("Convert"
                                          "原神！启动")
        self.button_convert.clicked.connect(self.convert_json_to_txt)
        self.layout.addWidget(self.button_convert)

        self.setLayout(self.layout)

    def browse_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.folder_path:
            self.label_folder.setText(f"Selected folder: {self.folder_path}")

    def select_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if self.output_folder:
            self.label_output_folder.setText(f"Output folder: {self.output_folder}")

    def convert_json_to_txt(self):
        class_labels = self.input_class.text().split(';')
        class_map = {label.strip(): idx for idx, label in enumerate(class_labels)}

        image_width = int(self.input_width.text())
        image_height = int(self.input_height.text())
        decimal_places = 6

        if hasattr(self, 'folder_path') and hasattr(self, 'output_folder'):
            for file_name in os.listdir(self.folder_path):
                if file_name.endswith('.json'):
                    json_file_path = os.path.join(self.folder_path, file_name)
                    txt_file_path = os.path.join(self.output_folder, os.path.splitext(file_name)[0] + '.txt')
                    self.labelme_polygon_to_yolo_segmentation(json_file_path, txt_file_path, class_map, image_width,
                                                              image_height, decimal_places)

            print("Conversion complete.")

    def labelme_polygon_to_yolo_segmentation(self, labelme_json_file, yolo_txt_file, class_map, image_width, image_height, decimal_places=6):
        with open(labelme_json_file, 'r', encoding='utf-8') as f:
            labelme_data = json.load(f)

        with open(yolo_txt_file, 'w') as f:
            for shape in labelme_data['shapes']:
                class_label = shape['label']
                class_id = class_map.get(class_label, -1)
                if class_id == -1:
                    print(f"Class '{class_label}' not found in class map.")
                    continue

                normalized_segmentation = self.normalize_segmentation(shape['points'], image_width, image_height, decimal_places)

                f.write(f"{class_id} {' '.join(str(coord) for coord in normalized_segmentation)}\n")

    def normalize_segmentation(self, segmentation_points, image_width, image_height, decimal_places=6):
        normalized_segmentation = []
        for point in segmentation_points:
            normalized_x = round(point[0] / image_width, decimal_places)
            normalized_y = round(point[1] / image_height, decimal_places)
            normalized_segmentation.extend([normalized_x, normalized_y])
        return normalized_segmentation

if __name__ == '__main__':
    app = QApplication([])
    converter = JsonToTxtConverter()
    converter.show()
    app.exec_()