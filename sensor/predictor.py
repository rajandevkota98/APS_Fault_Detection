import os,sys
from sensor.exception import SensorException
from sensor.entity.config_entity import TARGET_ENCODER_OBJECT_FILE_NAME,TRANSFORMATION_OBJECT_FILE_NAME,MODEL_FILE_NAME
from glob import glob
from typing import Optional


class ModelResolver:

    def __init__(self, model_registry:str = "saved_models",transformer_model_dir_name="transformer", target_encoder_dirname="target_encoder",model_dir_name = "model"):
        self.model_registry = model_registry
        self.transformer_model_dir_name = transformer_model_dir_name
        self.target_encoder_dirname= target_encoder_dirname
        self.model_dir_name = model_dir_name
        os.makedirs(self.model_registry, exist_ok= True)

    def get_latest_dir_path(self,)->Optional[str]:
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names)==0:
                return None
            dir_names = list(map(int,dir_names))
            latest_folder_name=max(dir_names)
            return os.path.join(self.model_registry, f"{latest_folder_name}")
        except Exception as e:
            raise SensorException(e,sys)


    def get_latest_model_path(self,):
        try:
            latest_dir = self.get_latest_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise SensorException(e,sys)


    def get_latest_transformer_path(self,):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transformer is not available")
            return os.path.join(latest_dir,self.transformer_model_dir_name, TRANSFORMATION_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e,sys)

    def get_latest_target_encoder_path(self,):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Target encoder is not available.")
            return os.path.join(latest_dir,self.target_encoder_dirname,TARGET_ENCODER_OBJECT_FILE_NAME )
        except Exception as e:
            raise SensorException(e,sys)


    def get_latest_saved_dir_path(self,)->Optional[str]:
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                return os.path.join(self.model_registry, f"{0}")
            latest_dir_num = os.path.basename(self.get_latest_dir_path())
            return os.path.join(self.model_dir_name, f"{latest_dir_num+1}")
        except Exception as e:
            raise SensorException(e,sys)


    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_saved_dir_path()
            return os.path.join(latest_dir, self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise SensorException(sys,e)


    def get_latest_save_transformer_path(self):
        try:
            latest_dir = self.get_latest_saved_dir_path()
            return os.path.join(latest_dir, self.transformer_model_dir_name,TRANSFORMATION_OBJECT_FILE_NAME)

        except Exception as e:
            raise SensorException(sys, e)


    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_saved_dir_path()
            return os.path.join(latest_dir, self.target_encoder_dirname,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(sys, e)



    