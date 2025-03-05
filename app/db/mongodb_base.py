import pymongo
import traceback

from typing import List
from pymongo import MongoClient
from app.logs.log_handler import LogHandler
from app.utils.status_code import StatusCode


class MongoDB:
    client = None
    logger = None

    def setup_db(
            self,
            username: str,
            password: str,
            host: str,
            port: int,
            auth: str
        ):
        """
        Sets up the MongoDB connection with the provided credentials and host information.

        Args:
            username (str): The username for MongoDB authentication.
            password (str): The password for MongoDB authentication.
            host (str): The host address of the MongoDB server.
            port (int): The port number on which the MongoDB server is running.
            auth (str): The authentication source for MongoDB.
        """
        self.__class__.logger = LogHandler.get_logger("general")
        if auth is None:
            try:
                self.__class__.client = MongoClient(host=host,
                                                    port=port,
                                                    username=username,
                                                    password=password)
                self.logger.success("Initialize mongodb success")
            except Exception as e:
                self.logger.error(f"Initialize mongodb fail with following error: {e}")
        else:
            try:
                self.__class__.client = MongoClient(host=host,
                                                    port=port,
                                                    username=username,
                                                    password=password,
                                                    authSource=auth)
                self.logger.success("Initialize mongodb success")
            except Exception as e:
                self.logger.error(f"Initialize mongodb fail with following error: {e}")   

    @classmethod
    def insert_one(
            self,
            db_name: str,
            col_name: str,
            document: dict
        ):
        """
        Inserts a single document into the specified collection.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            document (dict): The document to be inserted.

        Returns:
            dict: A dictionary with the status of the operation.
        """
        col = self.client[db_name][col_name]
        try:
            col.insert_one(document)
            return {
                "status": True
            }
        except Exception as e:
            self.logger.error(f"An exception occurred insert_one: {traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }

    @classmethod
    def insert_many(
            self,
            db_name: str,
            col_name: str,
            documents: List[dict]
        ):
        """
        Inserts multiple documents into the specified collection.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            documents (List[dict]): The list of documents to be inserted.

        Returns:
            dict: A dictionary with the status of the operation.
        """
        col = self.client[db_name][col_name]
        try:
            col.insert_many(documents)
            return {
                "status": True,
            }
        except Exception as e:
            self.logger.error(f"An exception occurred insert_many: {traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }
    
    @classmethod
    def drop_collection(
            self,
            db_name: str,
            col_name: str
        ):
        """
        Drops the specified collection from the database.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection to be dropped.

        Returns:
            dict: A dictionary with the status of the operation.
        """
        try:
            collection_names = [n for n in self.client[db_name].list_collection_names()]
            if collection in collection_names:
                col = self.db[collection]
                col.drop()
                return {
                    "status": True
                }
            return {
                "status": True
            }

        except Exception as e:
            self.logger.error(f"An exception occurred drop_collection: {traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }
    
    @classmethod
    def delete_one(
            self,
            db_name: str,
            col_name: str,
            query: str
        ):
        """
        Deletes a single document from the specified collection that matches the query.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            query (str): The query to match the document to be deleted.

        Returns:
            dict: A dictionary with the status of the operation.
        """
        try:
            collection_names = [n for n in self.client[db_name].list_collection_names()]
            if col_name in collection_names:
                col = self.client[db_name][col_name]
                x = col.delete_one(query) 
                return {
                    "status": True
                }
            return {
                "status": True
            }
        except Exception as e:
            self.logger.error(f"An exception occurred delete_one:{traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }
        
    @classmethod
    def delete_many(
            self,
            db_name: str,
            col_name: str,
            query: str
        ):
        """
        Deletes multiple documents from the specified collection that match the query.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            query (str): The query to match the documents to be deleted.

        Returns:
            dict: A dictionary with the status of the operation.
        """
        try:
            collection_names = [n for n in self.client[db_name].list_collection_names()]
            if col_name in collection_names:
                col = self.client[db_name][col_name]
                x = col.delete_many(query)    
                return {
                    "status": True
                }
            return {
                "status": True
            }
        except Exception as e:
            self.logger.error(f"An exception occurred: {traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }

    @classmethod    
    def find_one(
            self,
            db_name: str,
            col_name: str,
            query: str
        ):
        """
        Finds a single document in the specified collection that matches the query.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            query (str): The query to match the document.

        Returns:
            dict: A dictionary with the status of the operation and the result if found.
        """
        try:
            col = self.client[db_name][col_name]
            result = col.find_one(query)
            if result:
                return {
                    "status": True,
                    "result": result
                }
            else:
                return {
                    "status": False,
                    "result": []
                }
        except Exception as e:
            self.logger.error(f"Find fail for query '{query}' with following error {traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }
    
    @classmethod
    def find(
            self,
            db_name: str,
            col_name: str,
            query: str,
            sort_data: list = None
        ):
        """
        Finds multiple documents in the specified collection that match the query.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            query (str): The query to match the documents.
            sort_data (list, optional): The list of sorting criteria.

        Returns:
            dict: A dictionary with the status of the operation and the result if found.
        """
        try:
            col = self.client[db_name][col_name]
            if sort_data is not None and len(sort_data)>0:
                result = list(col.find(query, {"_id": 0}).sort(sort_data))
            else:
                result = list(col.find(query, {"_id": 0}))
            if result:
                return {
                    "status": True,
                    "result": result
                }
            else:
                return {
                    "status": True,
                    "result": []
                }
        except Exception as e:
            self.logger.error(f"An exception occurred: {traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }

    @classmethod
    def update_one(
            self,
            db_name: str,
            col_name: str,
            query: str,
            document: dict
        ):
        """
        Updates a single document in the specified collection that matches the query.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            query (str): The query to match the document to be updated.
            document (dict): The new document data to update.

        Returns:
            dict: A dictionary with the status of the operation.
        """
        col = self.client[db_name][col_name]
        try:
            newvalues = { "$set": document }
            col.update_one(query, newvalues)
            return {
                "status": True
            }
        except Exception as e:
            self.logger.error(f"An exception occurred update_one: {traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }

    @classmethod
    def get_all_data(
            self,
            db_name: str,
            col_name: str
        ):         
        """
        Retrieves all documents from the specified collection.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.

        Returns:
            list: A list of all documents in the collection.
        """
        try:
            col = self.client[db_name][col_name]  
            result = list(col.find())
            return result
        except Exception as e:
            self.logger.error(f"An exception occurred get_all_data: {traceback.format_exc()}")
            return []
    
    @classmethod
    def update_or_insert_data(
            self, 
            db_name: str,
            col_name: str, 
            query: str, 
            document: dict
        ):
        """
        Updates or inserts a document in the specified collection based on the query.

        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            query (str): The query to match the document.
            document (dict): The document data to update or insert.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            col = self.client[db_name][col_name] 
            result = col.find_one(query)
            if result is not None:
                newvalues = { "$set": document }
                col.update_one(query, newvalues)
                return True
            else:
                self.insert_one(db_name=db_name, col_name=col_name, document=document)
                return True
        except Exception as e:
            self.logger.error(f"An exception occurred update_or_insert_data: {traceback.format_exc()}")
            return False

    @classmethod
    def update_or_insert_data_many(
            self, 
            db_name, 
            col_name,
            query, 
            document
        ):
        """
        Updates or inserts multiple documents in a MongoDB collection based on a query.
        If documents matching the query are found, they are updated with the provided document.
        If no matching documents are found, a new document is inserted.
        Args:
            db_name (str): The name of the database.
            col_name (str): The name of the collection.
            query (dict): The query to match documents.
            document (dict): The document to insert or update with.
        Returns:
            dict: A dictionary with the status of the operation. If successful, returns {"status": True}.
                    If an exception occurs, returns {"status": False, "error": Exception}.
        """
        try:
            col = self.client[db_name][col_name]
            result = col.find_one(query)
            if result is not None:
                newvalues = { "$set": document }
                col.update_many(query, newvalues)
                return {
                    "status": True
                }
            else:
                self.insert_document(db_name=db_name, col_name=col_name, document=document)
                return {
                    "status": True
                }
        except Exception as e:
            self.logger.error(f"An exception occurred update_or_insert_data: {traceback.format_exc()}")
            return {
                "status": False,
                "error": e
            }

def initialize_mongodb(
        host: str,
        port: int,
        username: str,
        password: str,
        auth: str
    ):
    """
    Initializes the MongoDB connection with the provided credentials and host information.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number on which the MongoDB server is running.
        username (str): The username for MongoDB authentication.
        password (str): The password for MongoDB authentication.
        auth (str): The authentication source for MongoDB.
    """    
    mdb = MongoDB()
    mdb.setup_db(username=username,
                 password=password,
                 host=host,
                 port=port,
                 auth=auth)