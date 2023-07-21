from argparse import ArgumentParser
from pathlib import Path

readme_txt = """# {name}

## Table of Contents

0. [Resources](#resources)

## Resources

- [Video]()
- [PDF](./docs/)
- [Online PDF]()
- [Session Notebook]()

## Topics
"""


def create_folder_with_files(name):
    # Create the main folder
    folder_path = Path(name)

    try:
        folder_path.mkdir(parents=True)
    except FileExistsError as e:
        return print(e)

    # Create empty files
    readme_fp = folder_path / 'README.md'
    with open(readme_fp, 'w') as f:
        f.write(readme_txt.format(name=name))

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

    # DEMO
    # $ python3 create_new_folder.py -n "Naive Bayes"
