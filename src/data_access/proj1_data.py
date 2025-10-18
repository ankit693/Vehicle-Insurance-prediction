# import sys
# import pandas as pd
# import numpy as np
# from typing import Optional

# from src.configuration.mongo_db_connection import MongoDBClient
# from src.constants import DATABASE_NAME
# from src.exception import MyException

# class Proj1Data:
#     """
#     A class to export MongoDB records as a pandas DataFrame.
#     """

#     def __init__(self) -> None:
#         """
#         Initializes the MongoDB client connection.
#         """
#         try:
#             self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
#         except Exception as e:
#             raise MyException(e, sys)

#     def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
#         """
#         Exports an entire MongoDB collection as a pandas DataFrame.

#         Parameters:
#         ----------
#         collection_name : str
#             The name of the MongoDB collection to export.
#         database_name : Optional[str]
#             Name of the database (optional). Defaults to DATABASE_NAME.

#         Returns:
#         -------
#         pd.DataFrame
#             DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
#         """
#         try:
#             # Access specified collection from the default or specified database
#             if database_name is None:
#                 collection = self.mongo_client.database[collection_name]
#             else:
#                 collection = self.mongo_client[database_name][collection_name]

#             # Convert collection data to DataFrame and preprocess
#             print("Fetching data from mongoDB")
#             df = pd.DataFrame(list(collection.find()))
#             print(f"Data fecthed with len: {len(df)}")
#             if "id" in df.columns.to_list():
#                 df = df.drop(columns=["id"], axis=1)
#             df.replace({"na":np.nan},inplace=True)
#             return df

#         except Exception as e:
#             raise MyException(e, sys)

import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException

class Proj1Data:
    """
    A class to export MongoDB records as a pandas DataFrame.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB client connection.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            # Access specified collection from the default or specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Fetch the documents from MongoDB
            print("🔍 Fetching documents from MongoDB collection...")
            documents = list(collection.find())
            print(f"📄 Number of documents fetched: {len(documents)}")

            if len(documents) > 0:
                print(f"🧾 Sample document:\n{documents[0]}")
            else:
                print("⚠️ No documents found in the collection.")

            # Convert to DataFrame
            df = pd.DataFrame(documents)
            print(f"🧮 DataFrame shape after loading: {df.shape}")
            print(f"📊 Columns in DataFrame: {df.columns.tolist()}")

            # Drop 'id' column if it exists
            if "id" in df.columns:
                df.drop(columns=["id"], inplace=True)
                print("🗑 Dropped 'id' column")

            # Replace "na" with np.nan
            df.replace({"na": np.nan}, inplace=True)

            # Drop '_id' column if present (optional)
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)
                print("🗑 Dropped '_id' column")

            print(f"✅ Final DataFrame shape: {df.shape}")
            return df

        except Exception as e:
            raise MyException(e, sys)
