import os
import json

def convert_text_to_array(json_file_path):
    for filename in os.listdir(json_file_path):
        if filename.endswith('.json'):  
            file_path = os.path.join(json_file_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)

            for shape in data['shapes']:
                shape['text'] = []

            with open(file_path, 'w') as file:  # Corrected line
                json.dump(data, file, indent=2)

if __name__ == "__main__":

    # Đổi lại tên folder chính giúp tôi

    folder_path = r'C:\AppLabelling\TestFiles' 

    # Xem thư mục của ông nằm trong khoảng bao nhiêu thì thay vô

    for i in range(114, 238):

        final_path = os.path.join(folder_path, str(i+1))
        convert_text_to_array(folder_path)
