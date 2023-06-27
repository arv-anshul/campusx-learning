from argparse import ArgumentParser
from pathlib import Path


def create_folder_with_files(name):
    # Create the main folder
    folder_path = Path(name)

    try:
        folder_path.mkdir(parents=True)
    except FileExistsError as e:
        return print(e)

    # Create empty files
    (folder_path / 'README.md').touch()

    # Create folders
    (folder_path / 'docs').mkdir(exist_ok=True)
    (folder_path / 'notebook').mkdir(exist_ok=True)

    print(f"Folder '{name}' with files and folders created successfully.")


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Create a folder with empty files and folders.'
    )
    parser.add_argument('-n', '--name', type=str,
                        help='Name of the folder to create', required=True)
    args = parser.parse_args()

    create_folder_with_files(args.name)
