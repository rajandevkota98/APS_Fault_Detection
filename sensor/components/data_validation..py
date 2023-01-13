from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
from scipy.stats import ks_2samp
from typing import Optional

class DataValidation:
    def __init__(self, data_validation_config:config_entity.DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation started {'<<'*20}")
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise SensorException(e,sys)



    def drop_missing_values_columns(self,df:pd.DataFrame, threshold:float= 0.3)->Optional[pd.DataFrame]:

        """
        This functions will dorp column which has a missing values more than threshold.
        df: Accepts a pandas dataframe
        threshold: Percentage criteria to drop a columns
        returns pandas Dataframe if atleast a single column is available
        else it will return a null value 
        """
        try:
            drop_column_names = []
            null_report = df.isna().sum()/df.shape[0]
            #selecting the columns which contains more than 30% null values
            drop_column_names = null_report[null_report>0.7].index
            df.drop(list(drop_column_names), axis = 1, inplace= True)

            if len(df.columns) ==0:
                return None
            else:
                return df


    def is_required_columns_exists(self,)->bool:
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)



        except Exception as e:
            raise SensorException(e,sys)




        


    def initiate_data_validation(self)-> artifact_entity.DataValidationArtifact:
        pass