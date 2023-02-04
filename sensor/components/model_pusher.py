from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
from scipy.stats import ks_2samp
from typing import Optional
from sensor.utils import write_yaml_file, convert_column_float
import numpy as np
from sensor.utils import load_object,save_object
from sensor.predictor import ModelResolver


from sensor.predictor import ModelResolver

class ModelPusher:
    logging.info("entering to model pusher")
    def __init__(self, model_pusher_config: config_entity.ModelPusherConfig,
    data_transformation_artifact: artifact_entity.DataTransformationArtifact,
    model_trainer_artifact: artifact_entity.ModelTrainerArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact =model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)

        except Exception as e:
            raise SensorException(e,sys)
    

    def initiate_model_pusher(self,)->artifact_entity.ModelPusherArtifact:
        try:
            #load object
            logging.info(f'loading transformer model and target encoder')
            transformer = load_object(file_path= self.data_transformation_artifact.transformation_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.label_enocoder_path)

            #model pusher dr
            logging.info("saving in model pusher dir" )
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj= transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj= model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj= target_encoder)


            #saved model dir
            logging.info("creating variable")
            model_path =self.model_resolver.get_latest_save_model_path()
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()
            transformer_path = self.model_resolver.get_latest_save_transformer_path()




            save_object(file_path=transformer_path, obj= transformer)
            save_object(file_path=model_path, obj= model)
            save_object(file_path=target_encoder_path, obj= target_encoder)


            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir = self.model_pusher_config.pusher_model_dir,
            saved_model_dir= self.model_pusher_config.saved_model_dir)


            return model_pusher_artifact


        except Exception as e:
            raise SensorException(e,sys)