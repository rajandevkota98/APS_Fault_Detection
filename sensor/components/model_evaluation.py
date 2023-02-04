from sensor.predictor import ModelResolver
from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils import load_object
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score
from sensor.config import TARGET_COLUMN
import os, sys
import pandas as pd
class ModelEvaluation:
    def __init__(self,model_evaluation_config: config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact: artifact_entity.DataTransformationArtifact,
        model_trainer_artifact: artifact_entity.ModelTrainerArtifact):

        try:
            logging.info("Model Evalutaion Started")
            self.model_evaluation_config =  model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise SensorException(e,sys)


    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            ##if saved model has moel then we will compare which model is best trained
            #or previous saved model
            logging.info("reading the latest dir")
            latest_dir_path = self.model_resolver.get_latest_dir_path()

            if latest_dir_path == None:
                logging.info("only model is present")
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(
                    is_model_accepted= True,
                    improved__accuracy= None
                )
                return model_evaluation_artifact


            #finding location of transformer model and target encoder
            #from previous 

            logging.info('reading the previous transformer, model and target encoder path')
            transformer_path =self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            logging.info('loading  previous trained transformer model and target_encoder')
            transformer = load_object(transformer_path)
            model = load_object(model_path)
            target_encoder = load_object(target_encoder_path)


            #currently_trained_model_objects
            logging.info('loading the current transformer')
            current_transformer = load_object(file_path=self.data_transformation_artifact.transformation_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.label_enocoder_path)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true =target_encoder.transform(target_df)


            # accuracy using previous trained model
            input_feature_name = list(transformer.feature_names_in_)
            input_arr =transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            print(f"Prediction using previous model: {target_encoder.inverse_transform(y_pred[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")


            ##usinh current trained model
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr =current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            print(f"Prediction using trained model: {current_target_encoder.inverse_transform(y_pred[:5])}")
            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")
            logging.info(f"Previous:{previous_model_score}")
            logging.info(f"Current: {current_model_score}")
            if current_model_score<previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            logging.info(f"Previous:{previous_model_score}")
            logging.info(f"Current: {current_model_score}")
            model_evaluation_artifact =  artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,improved__accuracy=current_model_score - previous_model_score )
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")

            return model_evaluation_artifact

            

            












            





            
        except Exception as e:
            raise SensorException(e,sys)

