"""
Module `cache` contains the `Cache` class which is used to
temporarily store JSON documents.
"""

import dataclasses
import json

from __future__ import annotations


@dataclasses.dataclass(slots=True, kw_only=False, repr=True)
class Cache:
    """
    Class `Cache` stores database files in fields. Class `Client` has
    a cache attribute that stores an instance of this class, which is
    used in extensions and helpers to access the database.
    """
    blacklist: dict = dataclasses.field(default_factory=dict)
    reaction_roles: dict = dataclasses.field(default_factory=dict)

    @classmethod
    def from_database_filepaths(cls, database_filepaths: dict[str]) -> Cache:
        """
        Creates a `Cache` instance and populates the fields
        associated with the JSON documents passed in with their data.

        Pass in the filepaths to the blacklist and reaction role
        JSON documents. These can be located anywhere.

        Params:
         - database_filepaths (list[str]): Paths to the JSON documents.

        Returns
         - A `Cache` instance, with fields populated by the JSON documents.
        """
        temporary_cache = {}

        for document_name, document_filepath in database_filepaths.items():
            with open(document_filepath, "r") as document:
                temporary_cache[document_name] = json.load(document)

        return cls(**temporary_cache)