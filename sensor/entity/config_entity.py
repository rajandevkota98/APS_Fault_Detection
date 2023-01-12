
import os
from sensor.exception import SensorException
class TrainingPipelineConfig:
    def __init__(self):
        # self.artifact_dir = os.path.join(os.getcwd(),"artifact", f"{datetime.now().strftime('%m%d%Y__%H_%M_%S)}")
        self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")



class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.database_name = "aps"
        self.collection_dir = "sensor"
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
        self.feature_store_dir = os.path.join(self.data_ingestion_dir, "feature_store")
        self.train_file_path = os.path.join(self.data_ingestion_dir, "train_file")
        self.test_file_path = os.path.join(self.data_ingestion_dir,"test_dir")


    def to_dict()->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e, sys)


class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...