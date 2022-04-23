import abc
import os
import uuid
import zipfile

import pandas as pd


def zip_files(files, dirname):
    save_file = os.path.join(dirname, f"{uuid.uuid4()}.zip")
    with zipfile.ZipFile(save_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.write(filename=file, arcname=os.path.basename(file))
    return save_file


def remove_files(files):
    for file in files:
        os.remove(file)


class Writer(abc.ABC):
    extension = ""

    @staticmethod
    @abc.abstractmethod
    def write(file, dataset: pd.DataFrame):
        raise NotImplementedError("Please implement this method in the subclass.")


class CsvWriter(Writer):
    extension = "csv"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_csv(file, index=False, encoding="utf-8")


class JsonWriter(Writer):
    extension = "json"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_json(file, orient="records", force_ascii=False)


class JsonlWriter(Writer):
    extension = "jsonl"

    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_json(file, orient="records", force_ascii=False, lines=True)
