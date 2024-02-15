import os

for i in range(0, 100):
    # Specify the path for the new folder
    new_folder_path = f'D:\\Documents\\Gologin_Profile\\extensions\\profile_{i + 1}'

    # Create the new folder
    try:
        os.mkdir(new_folder_path)
        print(f"Folder '{new_folder_path}' created successfully!")
    except OSError as e:
        print(f"Error: {e}")
