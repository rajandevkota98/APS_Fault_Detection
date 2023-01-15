from sensor.utils import get_collection_as_dataframe
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor import utils
import sys,os
import pandas as pd
import numpy as  np
from sklearn.model_selection import train_test_split
# /home/rajan/python/APS_Fault_Detection/sensor/components/DataIngestion.py

class DataIngestion:
    def __init__(self, data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)


    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            #exporting collection data as pandas dataframe
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name= self.data_ingestion_config.database_name,
                collection_name = self.data_ingestion_config.collection_name)

            logging.info("Save data in feature store")
            #removing null values
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            #feature store file path
            logging.info("Create feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok = True)
            

            #save df in feature store folder
            logging.info("Save df to feature store folder")
            df.to_csv(path_or_buf = self.data_ingestion_config.feature_store_file_path, index = False , header = True)
            

            logging.info("Train test split")
            ##split dataset into two 
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size)

            #create dataset directory if not available 
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)
            #saving train dataframe
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            #saving test dataframe
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            #Prepare artifact

            logging.info("logging artifact")
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e,sys)

