import os


def create_archive_folder(base_folder, subfolder):
    # Create the path to the "Archivefolder" within the subfolder
    archive_folder_path = os.path.join(base_folder, subfolder, 'Archivefolder')

    # Check if the "Archivefolder" already exists
    if not os.path.exists(archive_folder_path):
        os.makedirs(archive_folder_path)
        print(f'Archivefolder created for {subfolder}')


def create_archive_folders():
    base_folder = "myproject/Application Files"  # Replace with the actual base folder path

    # Loop through each subfolder (samplefile1, samplefile2, samplefile3)
    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        # Check if the item is a directory (not a file)
        if os.path.isdir(subfolder_path):
            create_archive_folder(base_folder, subfolder)


if __name__ == "__main__":
    create_archive_folders()
