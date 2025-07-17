from typing import Dict

import duckdb
from hydra_zen import zen
from hydra_zen.third_party.pydantic import pydantic_parser
import kagglehub
import pydantic
from pydantic import BaseModel

from dummy_model.config import PROJ_ROOT


class DataIngestion(pydantic.BaseModel):

    def get_data_from_kaggle(kaggle_dataset: str, path: str = None):
        return kagglehub.dataset_download(kaggle_dataset, path=path)

    def write_raw_data(input_path: str, output_table_name: str = None):
        return duckdb.sql(
            f"""
            SELECT *
            FROM '{input_path}'
            """
        )


class MyConfig(BaseModel):
    from_kaggle: Dict[str, str]


@zen(instantiation_wrapper=pydantic_parser)
def my_app(data: MyConfig):
    input_path = DataIngestion.get_data_from_kaggle(
        data.from_kaggle["dataset"],
        data.from_kaggle["file_name"] 
    )
    print(DataIngestion.write_raw_data(input_path))


if __name__ == "__main__":
    my_app.hydra_main(
        version_base=None,
        config_path=f"{PROJ_ROOT}/conf",
        config_name="config"
    )
