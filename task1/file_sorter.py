import concurrent.futures
import os
import shutil
import sys


def get_extension(file_path):
    return os.path.splitext(file_path)[1].lstrip(".").lower() or "other"


def process_single_file(source_file_path, destination_folder):
    try:
        file_name = os.path.basename(source_file_path)
        file_extension = get_extension(source_file_path)
        extension_dir = os.path.join(destination_folder, file_extension)

        os.makedirs(extension_dir, exist_ok=True)
        shutil.copy2(source_file_path, os.path.join(extension_dir, file_name))
    except Exception as e:
        print(f"Error copying {source_file_path}: {e}")


def process_directory(source_folder, destination_folder):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                executor.submit(
                    process_single_file, source_file_path, destination_folder
                )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sorter.py <source_folder> [destination_folder]")
        sys.exit(1)

    source = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else "dist"

    if not os.path.isdir(source):
        print(f"Error: Source folder '{source}' does not exist.")
        sys.exit(1)

    os.makedirs(destination, exist_ok=True)
    process_directory(source, destination)
    print("File processing completed successfully.")
