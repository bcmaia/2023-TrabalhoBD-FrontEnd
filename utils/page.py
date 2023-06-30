import os


def read_files_to_dict(folder_path):
    file_dict = {}

    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if the path points to a file
        if os.path.isfile(file_path):
            # Extract the file name without extension
            file_name_without_extension = os.path.splitext(file_name)[0]

            # Check for collisions
            if file_name_without_extension in file_dict:
                raise ValueError(f"Collision occurred: '{file_name_without_extension}' already exists in the dictionary.")

            with open(file_path, 'r') as file:
                # Read the contents of the file
                file_content = file.read()

                # Add the file name without extension and content to the dictionary
                file_dict[file_name_without_extension] = file_content

    return file_dict




pages = read_files_to_dict('./pages')



def show (page_name):
    print(pages[page_name], end='')

