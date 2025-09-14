import os
import json


def labelme_polygon_to_yolo_segmentation(labelme_json_file, yolo_txt_file, class_map, image_width, image_height,
                                         decimal_places=6):
    with open(labelme_json_file, 'r', encoding='utf-8') as f:
        labelme_data = json.load(f)

    with open(yolo_txt_file, 'w') as f:
        for shape in labelme_data['shapes']:
            class_label = shape['label']
            class_id = class_map.get(class_label, -1)
            if class_id == -1:
                print(f"Class '{class_label}' not found in class map.")
                continue

            # Normalize coordinates to range [0, 1] with specified decimal places
            normalized_segmentation = normalize_segmentation(shape['points'], image_width, image_height, decimal_places)

            # Write YOLO format annotation to file
            f.write(f"{class_id} {' '.join(str(coord) for coord in normalized_segmentation)}\n")


def normalize_segmentation(segmentation_points, image_width, image_height, decimal_places=6):
    normalized_segmentation = []
    for point in segmentation_points:
        normalized_x = round(point[0] / image_width, decimal_places)
        normalized_y = round(point[1] / image_height, decimal_places)
        normalized_segmentation.extend([normalized_x, normalized_y])
    return normalized_segmentation


def convert_folder_json_to_yolo(folder_path, class_map, image_width, image_height, decimal_places=6):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(folder_path, file_name)
            txt_file_path = os.path.splitext(json_file_path)[0] + '.txt'
            labelme_polygon_to_yolo_segmentation(json_file_path, txt_file_path, class_map, image_width, image_height,
                                                 decimal_places)


# Usage example
class_map = {'blackline': 0, 'deadknot': 1, 'gap': 2}  # Mapping from class labels to class ids
image_width = 5472  # Example image width
image_height = 3648  # Example image height
decimal_places = 5  # Number of decimal places to round to 小数点保留
folder_path = 'D:\\YOLO\\pythonProject\\wood\\'
convert_folder_json_to_yolo(folder_path, class_map, image_width, image_height, decimal_places)





