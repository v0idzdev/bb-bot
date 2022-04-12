"""
Module `document` contains the `Document` class, which aims to
hide lower-level details of interacting with MongoDB. It provides
a simple API we can use in other files.
"""
import logging
import collections.abc


class Document:
    """
    Class`Document` aims to make using mongo easier, and abstracts
    lower-level details. Pass in the db instance on initialization and
    add the document to create an instance of.
    """
    def __init__(self, connection, document_name) -> None:
        """
        Creates a connection to the specified document.

        Params:
         - connection (Mongo Connection): Our Mongo DB connection.
         - document_name (str): The document this instance should be.

        Returns:
         - A `Document` instance.
        """
        self.db = connection[document_name]
        self.logger = logging.getLogger(__name__)

    # Public methods
    async def update(self, dict) -> None:
        """
        For when a document already exists in the data and
        you want to update something in it.

        This function parses an input Dictionary to get the
        relevant information needed to update.

        Params:
         - dict (Dictionary): The dictionary to insert.

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
        await self.db.update_one({"_id": dict["_id"]}, {"$set": dict})

    async def find(self, id):
        """
        Returns the data found under `id`.

        Params:
         - id (): The ID to search for.

        Returns:
         - None if nothing is found.
         - If something is found, return it.
        """
        return await self.db.find_one({"_id": id})

    async def delete(self, id):
        """
        Deletes all items found with _id: `id`.

        Params:
         - id (): The ID to search for and delete.
        """
        if not await self.find(id):
            pass

        await self.db.delete_many({"_id": id})

    async def insert(self, dict):
        """
        Inserts data into the database.

        Params:
         - dict (Dictionary): The dictionary to insert.

        Raises:
         - TypeError if `dict` is not a dictionary.
         - KeyError if _id was not found.
        """
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected a dictionary.")

        if not dict["_id"]:
            raise KeyError("_id was not found in the supplied dictionary.")

        await self.db.insert_one(dict)

    async def upsert(self, dict):
        """
        Creates a new item in the document, if it already exists
        it will update that item instead.

        This method parses an input Dictionary to get the
        relevant information needed to insert. Supports
        inserting when the document already exists.

        Params:
         - dict (Dictionary): The dictionary to insert.
        """
        if await self.__get_raw(dict["_id"]) != None:
            await self.update(dict)

        else:
            await self.db.insert_one(dict)

    async def unset(self, dict):
        """
        For when you want to remove a field from a
        pre-existing document in the collection.

        This method parses an input Dictionary to get the
        relevant information needed to unset.

        Params:
         - dict (Dictionary): The dictionary for parse for info.

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
        await self.db.update_one({"_id": id}, {"$unset": dict})

    async def increment(self, id, field, amount):
        """
        Increment a given `field` by `amount`.

        Params:
         - id (): The ID to search for.
         - field (): The field to increment.
         - amount (int): The amount to increment.
        """
        if not await self.find(id):
            pass

        self.db.update_one({"_id": id}, {"$inc": {field: amount}})

    async def get_all(self):
        """
        Returns a list of all data in the document.

        Returns:
         - The list of all data in the document.
        """
        data = []

        async for document in self.db.find({}):
            data.append(document)

        return data

    # Private methods
    async def __get_raw(self, id):
        """
        Internal method used to evaluate certain checks within
        other methods that require the actual data.
        """
        return await self.db.find_one({"_id": id})