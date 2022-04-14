"""
Module `apis.mongo.collection` contains the `Collection` class, which
aims to hide lower-level details of interacting with MongoDB. It provides
a simple API we can use in other files.
"""
import collections.abc
import motor.motor_asyncio

from typing import Any


class Collection:
    """
    Class `Collection` aims to make using mongo easier, and abstracts
    lower level details. Pass in the db instance on initialization and
    add the collection to create an instance of.
    """
    def __init__(self, database: motor.motor_asyncio.AsyncIOMotorDatabase, collection_name: str) -> None:
        """
        Creates an instance of the specified collection. A collection is
        a file containing documents, which act like individual rows. A
        collection, therefore, acts like a table.

        Params:
         - connection (Mongo Connection): Our Mongo DB connection.
         - document_name (str): The document this instance should be.

        Returns:
         - A `Document` instance.
        """
        self._collection: motor.motor_asyncio.AsyncIOMotorCollection = database[collection_name]

    @property
    def collection(self) -> motor.motor_asyncio.AsyncIOMotorCollection:
        """
        Returns the AsyncIOMotorCollection object associated with this instance.
        It is recommended to use methods within this class as opposed to accessing
        the collection object directly.
        """
        return self._collection

    async def update(self, dict: collections.abc.Mapping) -> None:
        """
        For when a document already exists in the collection
        and you want to update something in it.

        This function parses an input Dictionary to get the
        relevant information needed to update.

        Params:
         - dict (collections.abc.Mapping): The dictionary to insert.

        Raises:
         - TypeError if `dict` is not a dictionary.
         - KeyError if _id was not found.
        """
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected a dictionary.")

        if not dict["_id"]:
            raise KeyError("_id not found in the supplied dictionary.")

        if not await self.find(dict["_id"]):
            pass

        dict.pop("_id")
        await self._collection.update_one({"_id": dict["_id"]}, {"$set": dict})

    async def find(self, id: Any):
        """
        Returns the data found under `id`.

        Params:
         - id (Any): The ID to search for.

        Returns:
         - None if nothing is found.
         - If something is found, return it.
        """
        return await self._collection.find_one({"_id": id})

    async def delete(self, id: Any):
        """
        Deletes all items found with _id: `id`.

        Params:
         - id (Any): The ID to search for and delete.
        """
        if not await self.find(id):
            pass

        await self._collection.delete_many({"_id": id})

    async def insert(self, dict: collections.abc.Mapping):
        """
        Inserts a document into the collection.

        Params:
         - dict (collections.abc.Mapping): The dictionary to insert.

        Raises:
         - TypeError if `dict` is not a dictionary.
         - KeyError if _id was not found.
        """
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected a dictionary.")

        if not dict["_id"]:
            raise KeyError("_id was not found in the supplied dictionary.")

        await self._collection.insert_one(dict)

    async def upsert(self, dict: collections.abc.Mapping):
        """
        Creates a new document in the collection, if it already
        exists it will update that item instead.

        This method parses an input Dictionary to get the
        relevant information needed to insert. Supports
        inserting when the document already exists.

        Params:
         - dict (collections.abc.Mapping): The dictionary to insert.
        """
        if await self.__get_raw(dict["_id"]) != None:
            await self.update(dict)

        else:
            await self._collection.insert_one(dict)

    async def unset(self, dict: collections.abc.Mapping):
        """
        For when you want to remove a field from a pre-existing
        document in the collection.

        This method parses an input Dictionary to get the
        relevant information needed to unset.

        Params:
         - dict (collections.abc.Mapping): The dictionary for parse for info.

        Raises:
         - TypeError if `dict` is not a dictionary.
         - KeyError if _id was not found.
        """
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected a dictionary.")

        if not dict["_id"]:
            raise KeyError("_id not found in the supplied dictionary.")

        if not await self.find(dict["_id"]):
            return

        dict.pop("_id")
        await self._collection.update_one({"_id": id}, {"$unset": dict})

    async def increment(self, id: Any, field: Any, amount: int):
        """
        Increment a given `field` by `amount`.

        Params:
         - id (): The document's ID number to search for.
         - field (): The field in the document to increment.
         - amount (int): The amount to increment it by.
        """
        if not await self.find(id):
            pass

        self._collection.update_one({"_id": id}, {"$inc": {field: amount}})

    async def get_all(self):
        """
        Returns a list of all data in the document.

        Returns:
         - The list of all data in the document.
        """
        data = []

        async for document in self._collection.find({}):
            data.append(document)

        return data

    # Private methods
    async def __get_raw(self, id: Any):
        """
        Internal method used to evaluate certain checks within
        other methods that require the actual data.
        """
        return await self._collection.find_one({"_id": id})