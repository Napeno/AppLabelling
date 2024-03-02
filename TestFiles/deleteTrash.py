import os

def delete_unmatched_files(folder_path):

    files = os.listdir(folder_path)
    
    json_files = [f for f in files if f.endswith('.json')]
    image_files = [f for f in files if f.endswith('.png') or f.endswith('.jpg')]

    json_names = [os.path.splitext(f)[0] for f in json_files]
    
    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        if base_name not in json_names:
            os.remove(os.path.join(folder_path, image_file))
            print(f"Deleted {image_file}")

folder_path = r'C:\AnyLabelling\Test'

for i in range(114, 238):
        final_path = os.path.join(folder_path, str(i+1))
        delete_unmatched_files(final_path)
