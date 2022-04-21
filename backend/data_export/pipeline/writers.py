import abc
import os
import uuid
import zipfile

import pandas as pd


def zip_files(files):
    save_file = f"{uuid.uuid4()}.zip"
    with zipfile.ZipFile(save_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.write(filename=file, arcname=os.path.basename(file))
    return save_file


class Writer(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def write(file, dataset: pd.DataFrame):
        raise NotImplementedError("Please implement this method in the subclass.")


class CsvWriter(Writer):
    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_csv(file, index=False, encoding="utf-8")


class JsonWriter(Writer):
    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_json(file, orient="records", force_ascii=False)


class JsonlWriter(Writer):
    @staticmethod
    def write(file, dataset: pd.DataFrame):
        dataset.to_json(file, orient="records", force_ascii=False, lines=True)
