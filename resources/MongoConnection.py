import os
from typing import List, Any, Dict

import pymongo
from bson import ObjectId
from dotenv import load_dotenv


class MongoConnection:

    def __init__(self, database='real-estate-project', collection='idealista') -> None:
        load_dotenv('.env')
        self.client = pymongo.MongoClient(os.getenv("MONGO_PASS"))
        self.database = database
        self.collection = collection
        self.db = self.client.get_database('hiklub')
        self.collection_list = self.db.list_collection_names()

    def set_collection(self, collection: str) -> None:
        setattr(self, 'collection', collection)

    def get_doc(self, query=None, project=None) -> List[Any]:
        if query is None:
            query = {}
        return list(self.db[self.collection].find(query, project))

    def get_docs_per_id(self, id_list: List[ObjectId], project=None) -> List[Dict[Any, Any]]:
        query = {'_id': {'$in': id_list}}
        return self.get_doc(query=query, project=project)

    def insert_doc(self, doc: dict) -> Dict[str, ObjectId]:
        curs = self.db[self.collection].insert_one(doc)
        return {"_id": curs.inserted_id}

    def insert_many_docs(self, docs: List[dict]):
        curs = self.db[self.collection].insert_many(docs)
        return {"_id": curs.inserted_ids}

    def update_publication(self, data: List[dict], identifier) -> int:
        curs = self.db[self.collection].update_one(
            {"_id": ObjectId(identifier)},
            {"$push": {"affinity": {"$each": data}}}
        )
        return curs.modified_count

    def delete_doc(self, filt: dict) -> int:
        curs = self.db[self.collection].delete_one(filt)
        return curs.deleted_count
