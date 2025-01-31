import concurrent.futures
import os
import shutil
import argparse


def get_extension(file_path):
    """Получает расширение файла без точки и в нижнем регистре."""
    return os.path.splitext(file_path)[1].lstrip(".").lower() or "other"


def process_single_file(source_file_path, destination_folder):
    """Копирует файл в соответствующую папку по расширению."""
    file_name = os.path.basename(source_file_path)
    file_extension = get_extension(source_file_path)

    extension_dir = os.path.join(destination_folder, file_extension)
    os.makedirs(extension_dir, exist_ok=True)

    destination_file_path = os.path.join(extension_dir, file_name)
    shutil.copy2(source_file_path, destination_file_path)


def process_directory(source_folder, destination_folder):
    """Обходит все файлы в папке и копирует их параллельно."""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for root, _, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                executor.submit(
                    process_single_file, source_file_path, destination_folder
                )


def main():
    parser = argparse.ArgumentParser(
        description="Sort files by extension in parallel."
    )  # так надо

    parser.add_argument("source_folder", type=str, help="Source folder path")
    parser.add_argument(
        "destination_folder",
        type=str,
        nargs="?",
        default="dist",
        help="Destination folder path (default: dist)",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.source_folder):
        raise NotADirectoryError(
            f"Source folder '{args.source_folder}' does not exist."
        )

    os.makedirs(args.destination_folder, exist_ok=True)

    process_directory(args.source_folder, args.destination_folder)
    print("File processing completed successfully.")


if __name__ == "__main__":
    main()
