from sensor.utils import get_collection_as_dataframe
from sensor.exception import SensorException
from sensor.logger import logging
import sys, os
from sensor.entity import config_entity
from datetime import datetime
from sensor.components.data_ingestion import  DataIngestion
from sensor.entity.config_entity import DataValidationConfig
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation

if __name__=="__main__":
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact )
          data_validation_artifact = data_validation.initiate_data_validation()

          logging.info("transformation started")
          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config =data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()


          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact = model_trainer.initiate_model_trainer()

          model_evaluation_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_evaluation = ModelEvaluation(model_evaluation_config=model_evaluation_config,data_ingestion_artifact=data_ingestion_artifact,data_transformation_artifact=data_transformation_artifact,model_trainer_artifact=model_trainer_artifact)
          model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

     except Exception as e:
          print(e)



