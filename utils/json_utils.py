import json

from pathlib import Path
from typing import Any, Union


def read_json_file(file_path: Union[str, Path]) -> Any:
    """
    Reads a JSON file and returns its content.

    :param file_path: Path to the JSON file.
    :return: Content of the JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json_file(file_path: Union[str, Path], data: Union[dict, list]) -> None:
    """
    Writes data to a JSON file.

    :param file_path: Path to the JSON file.
    :param data: The data to be written.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
