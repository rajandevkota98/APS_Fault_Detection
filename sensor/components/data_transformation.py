from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sklearn.pipeline import Pipeline
import os, sys
import pandas as pd
from typing import Optional
from sensor.utils import write_yaml_file, convert_column_float
import numpy as np
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sensor.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
from sensor import utils




class DataTransformation:
    def __init__(self, data_transformation_config: config_entity.DataTransformationConfig, data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f" {'**'*20} Starting of data Transformation {'**'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)

    ##when we use instance method,, we use self
    ##and we can create millions number of objects
    ########################################
    #in a class method, when we use class method, all the object have the access of it.

    @classmethod
    def get_class_transformer_object(cls)->Pipeline:

        try:
            simple_imputer = SimpleImputer(strategy="constant", fill_value= 0)

            robust_scaler = RobustScaler()
            pipeline = Pipeline(
                steps = [
                    (
                        'Imputer', simple_imputer
                    ),
                    (
                        'RobustScaler', robust_scaler
                    )
                ]
            )
            return pipeline
        except Exception as e:

            raise SensorException(e,sys)

    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:
        try:
            
            #reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)


            #splitting into dependent and independent features

            input_train_df = train_df.drop(TARGET_COLUMN,axis = 1)
            input_test_df = test_df.drop(TARGET_COLUMN, axis = 1)


            target_train_df = train_df[TARGET_COLUMN]
            target_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_train_df)

            #transformation of target columns
            target_train_array = label_encoder.transform(target_train_df)
            target_test_array = label_encoder.transform(target_test_df)

            #transforming input features


            transformation_pipeline = DataTransformation.get_class_transformer_object()
            transformation_pipeline.fit(input_train_df)

            input_feature_train_arr =transformation_pipeline.transform(input_train_df)
            input_feature_test_arr =transformation_pipeline.transform(input_test_df)


            #samping the minority that is negative values
            smt = SMOTETomek(sampling_strategy= "minority")
            logging.info(f"Before reshamping in training set input:----Input Feature {input_feature_train_arr.shape},  ---Target Feature{target_train_array.shape}")
            input_feature_train_arr,target_train_array= smt.fit_resample(input_feature_train_arr,target_train_array)
            logging.info(f"After reshamping in training set input:----Input Feature {input_feature_train_arr.shape},  ---Target Feature{target_train_array.shape}")
            logging.info(f"Before reshamping in Testing set input:----Input Feature {input_feature_test_arr.shape},  ---Target Feature{target_test_array.shape}")
            input_feature_test_arr,target_test_array= smt.fit_resample(input_feature_test_arr,target_test_array)
            logging.info(f"After reshamping in Testing set input:----Input Feature {input_feature_test_arr.shape},  ---Target Feature{target_test_array.shape}")

            #concat train array and test_array
            train_array = np.c_[input_feature_train_arr,target_train_array]
            test_array = np.c_[input_feature_test_arr,target_test_array]



            #save numoy array
            utils.save_numpy_array_data(file_path= self.data_transformation_config.transformed_train_path ,array=train_array)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformated_test_path, array=test_array)

            ##saving transformation pipeline object

            utils.save_object(file_path=self.data_transformation_config.transformation_object_path, obj= transformation_pipeline)


            utils.save_object(file_path=self.data_transformation_config.label_enocoder_path, obj= label_encoder)


            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
            transformation_object_path=self.data_transformation_config.transformation_object_path,
            transformed_train_path = self.data_transformation_config.transformed_train_path,
            transformated_test_path=self.data_transformation_config.transformated_test_path,
            label_enocoder_path = self.data_transformation_config.label_enocoder_path
                    

            )
            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

