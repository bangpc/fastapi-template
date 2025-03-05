from pydantic import BaseModel
from typing import Optional
from app.db import MongoDB

class User(MongoDB, BaseModel):
    _database_name: str = "project_name"
    _collection_name: str = "user"
    id: str
    name: str
    email: str
    password: str

    @classmethod
    def insert_one_user(
        self,
        data: dict = None
    ):
        """
        Inserts a new user document into the user collection.

        Args:
            data (dict, optional): The user data to insert. Defaults to None.

        Returns:
            InsertOneResult: The result of the insert operation.
        """
        return MongoDB.insert_one(
            self._database_name,
            self._collection_name,
            data
        )

    @classmethod
    def delete_one_user(
        self,
        data: dict = None
    ):
        """
        Deletes a user document from the user collection.

        Args:
            data (dict, optional): The user data to delete. Defaults to None.

        Returns:
            DeleteResult: The result of the delete operation.
        """
        return MongoDB.delete_one(
            self._database_name,
            self._collection_name,
            data
        )

    @classmethod
    def find_one_user(
        self,
        data: dict = None
    ):
        """_summary_

        Args:
            data (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return MongoDB.find_one(
            self._database_name,
            self._collection_name,
            data
        )


class UserGroup(MongoDB, BaseModel):
    _database_name: str = "aiss"
    _collection_name: str = "user_group"
    user_id: str
    group_id: str
    description: str

    @classmethod
    def insert_one_user_group(
        self,
        data: dict = None
    ):
        """_summary_

        Args:
            data (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return MongoDB.insert_one(
            self._database_name,
            self._collection_name,
            data
        )

    @classmethod
    def delete_one_user_group(
        self,
        data: dict = None
    ):
        """_summary_

        Args:
            data (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return MongoDB.delete_one(
            self._database_name,
            self._collection_name,
            data
        )

    @classmethod
    def find_one_user_group(
        self,
        data: dict = None
    ):
        """_summary_

        Args:
            data (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return MongoDB.find_one(
            self._database_name,
            self._collection_name,
            data
        )


class Group(MongoDB, BaseModel):
    _database_name: str = "aiss"
    _collection_name: str = "group"
    id: str
    name: str
    description: str

    @classmethod
    def insert_one_group(
        self,
        data: dict = None
    ):
        """_summary_

        Args:
            data (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return MongoDB.insert_one(
            self._database_name,
            self._collection_name,
            data
        )

    @classmethod
    def delete_one_group(
        self,
        data: dict = None
    ):
        """_summary_

        Args:
            data (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return MongoDB.delete_one(
            self._database_name,
            self._collection_name,
            data
        )

    @classmethod
    def find_one_group(
        self,
        data: dict = None
    ):
        """_summary_

        Args:
            data (dict, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return MongoDB.find_one(
            self._database_name,
            self._collection_name,
            data
        )
