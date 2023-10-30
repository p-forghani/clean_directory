import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Union

from loguru import logger
from tqdm import tqdm

from src.data import DATA_DIR


class CleanDirectory:
    def __init__(self, DIR_PATH: Union[str, Path]) -> None:
        """
        Initializes the CleanDirectory object.

        Args:
            DIR_PATH (str): Path to the directory containing
            the files to be organized.
        """
        self.directory = Path(DIR_PATH)

        # Create a dict to map extensions to categories from the json file
        self.file_map = defaultdict(lambda: 'Others')
        with open(DATA_DIR / 'extensions.json') as f:
            categories = json.load(f)
            for category, extensions in categories.items():
                for ext in extensions:
                    self.file_map[ext] = category

    def organize_files(self) -> None:
        """
        Organizes files in the directory based on their
        extensions and moves them to appropriate folders.
        """
        for file_path in tqdm(self.directory.iterdir(), position=0):
            # Ignore directories
            if file_path.is_dir():
                continue
            # Ignore hidden files
            if file_path.name.startswith('.'):
                continue
            # Create the destination path if it doesen't exist
            dest_path = self.directory / self.file_map[file_path.suffix]
            dest_path.mkdir(exist_ok=True)
            # Move the file to the proper directory
            shutil.move(file_path, dest_path)
            logger.info(f'{file_path.name} moved to the {self.file_map[file_path.suffix]} folder.')

if __name__ == "__main__":
    # Example usage:
    path = Path('PATH/TO/DIRECTORY')
    cleaner = CleanDirectory(path)
    cleaner.organize_files()
