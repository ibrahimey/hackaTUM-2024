import json
import os

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


def append_json_file(file_path: Union[str, Path], data: dict) -> None:
    """
    Appends data to a JSON file. Creates a new file if it does not exist or is empty.

    :param file_path: Path to the JSON file.
    :param data: The data to be appended.
    """
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        current_list = read_json_file(file_path)
        # current_list.extend(data)
        data.extend(current_list)
        current_list = data
    else:
        current_list = data
    write_json_file(file_path, current_list)
