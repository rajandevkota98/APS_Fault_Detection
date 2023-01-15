from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
from scipy.stats import ks_2samp
from typing import Optional
from sensor.utils import write_yaml_file
import numpy as np


class DataValidation:
    def __init__(self, data_validation_config:config_entity.DataValidationConfig,data_ingestion_artifact: artifact_entity.DataIngestionArtifact):

        try:
            logging.info(f"{'>>'*20} Data Validation started {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.validation_error = dict()
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise SensorException(e,sys)



    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:

        """
        This functions will dorp column which has a missing values more than threshold.
        df: Accepts a pandas dataframe
        threshold: Percentage criteria to drop a columns
        returns pandas Dataframe if atleast a single column is available
        else it will return a null value 
        """
        try:
            logging.info("dropping missing values columns")
            drop_column_names = []
            null_report = df.isna().sum()/df.shape[0]
            logging.info(f"selecting the columns which contains more than {self.data_validation_config.missing_threshold}  null values")
            #selecting the columns which contains more than 30% null values
            drop_column_names = null_report[null_report> self.data_validation_config.missing_threshold].index


            self.validation_error["dropped_columns" + report_key_name] = drop_column_names
            df.drop(list(drop_column_names), axis = 1, inplace= True)

            if len(df.columns) ==0:
                return None
            else:
                return df
        except Exception as e:
            raise SensorException(e ,sys)

    def is_required_columns_exists(self,base_df, current_df, report_key_name:str)->bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns
            missing_columns = []

            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_columns)
            if len(missing_columns) >0:
                self.validation_error["missing columsn" + report_key_name] = missing_columns

        except Exception as e:
            raise SensorException(e, sys)


    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns  

            for base_column in base_columns:
                base_data, current_data = base_df[base_column],current_df[base_column]
                is_same_distribution = ks_2samp(base_data,current_data)


                if is_same_distribution.pvalue > 0.05:
                    drift_report[base_column + report_key_name] = {
                        "pvalues": is_same_distribution.pvalue,
                        "is_same_distribution": True
                    }
                    #same distribution
                else:
                    drift_report[base_column + report_key_name] = {
                        "pvalues": is_same_distribution.pvalue,
                        "is_same_distribution": False
                    }

                    #different distribution

        except Exception as e:
            raise SensorException(e, sys)
        

    def initiate_data_validation(self)-> artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            #base data frame has na as null values as well

            base_df.replace({"na":np.NaN}, inplace= True)
            base_df = self.drop_missing_values_columns(df=base_df,report_key_name= "base")


            #reading the train file file path
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            train_df = self.drop_missing_values_columns(df = train_df, report_key_name=" train")

            logging.info("checking drop missing column in train file path")
            #reading test file path
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            test_df = self.drop_missing_values_columns(df = test_df, report_key_name="test")

            train_status = self.is_required_columns_exists(base_df= base_df, current_df= train_df, report_key_name="train")
            test_status = self.is_required_columns_exists(base_df= base_df, current_df= test_df, report_key_name="test")
        
            if train_status:
                self.data_drift(base_df=base_df, current_df= train_df, report_key_name=" data_drift_in_train")

            if test_status:
                self.data_drift(base_df= base_df,current_df=test_df,report_key_name= "data_drift_in_test")



            ###writing the report file

            logging.info("writing the yaml file")
            write_yaml_file(file_path=self.data_validation_config.report_file_path, data=self.validation_error)
            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)