from os import read
import jsonlines
from idealista.idealista_api import get_response_info, save_responses_as_jsonl
from resources.MongoConnection import MongoConnection


def get_new_data_from_idealista() -> str:
    info = get_response_info()
    file_name = save_responses_as_jsonl(pages_to_iter=info['totalPages'])
    return file_name


def publish_data(file_path: str):
    with jsonlines.open(file_path, mode='r') as reader:
        MongoConnection().insert_many_docs(list(reader))


if __name__ == "__main__":
    file_name = get_new_data_from_idealista()
    publish_data(file_name)
