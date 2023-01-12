



import os
from datetime import datetime
from sensor.exception import SensorException
FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
class TrainingPipelineConfig:
    def __init__(self):
        # self.artifact_dir = os.path.join(os.getcwd(),"artifact", f"{datetime.now().strftime('%m%d%Y__%H_%M_%S)}")
        self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")



class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.database_name = "aps"
        self.collection_name = "sensor"
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir, "feature_store", FILE_NAME)
        self.train_file_path = os.path.join(self.data_ingestion_dir, "train_file")
        self.test_file_path = os.path.join(self.data_ingestion_dir,"test_dir")

        self.test_size = 0.2
    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e, sys)


class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...