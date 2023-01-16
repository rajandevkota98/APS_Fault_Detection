from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
from scipy.stats import ks_2samp
from typing import Optional
from sensor.utils import write_yaml_file, convert_column_float
import numpy as np
from sensor.config import TARGET_COLUMN
from xgboost import XGBClassifier 
from sensor import utils
from sklearn.metrics import f1_score


class ModelTrainer:
    def __init__(self, model_trainer_config:config_entity.ModelTrainerConfig,
    data_transformation_artifact: artifact_entity.DataTransformationArtifact
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact= data_transformation_artifact

        except Exception as e:
            raise SensorException(e,sys)

    def train_model(self,X,y):
        Xg_clf = XGBClassifier()
        Xg_clf.fit(X,y)
        return Xg_clf


    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"loading training and test array")
            test_data = utils.load_numpy_data(self.data_transformation_artifact.transformated_test_path)
            train_data = utils.load_numpy_data(self.data_transformation_artifact.transformed_train_path)
            logging.info("spilting dependent and independent data columns")
            X_train = train_data[:,:-1]
            y_train = train_data[:,-1]

            X_test = test_data[:,:-1]
            y_test = test_data[:,-1]

            logging.info(f"{X_train.shape}, {y_train.shape}")
            ##training model
            logging.info(f"Model is training")
            model = self.train_model(X=X_train, y = y_train)

            ##yhat prediction
            yhat_train = model.predict(X_train)
            logging.info("model is trained")
            f1_train_score = f1_score(y_true=y_train, y_pred=yhat_train)
            
            logging.info(f"Traing f1 score:{f1_train_score}")


            #yhat test prediction
            yhat_test = model.predict(X_test)
            f1_test_score = f1_score(y_true=y_test,y_pred=yhat_test)
            logging.info(f"f1 test score: {f1_test_score}")

            #checking for overfitting or underfitting or expected score
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give exoected score actual score: {f1_test_score}  expected score {self.model_trainer_config.expected_score}")

            logging.info(f"The test is passed. Crossed the threshold")
            diff = abs(f1_train_score-f1_test_score)
            logging.info(f"The difference is less than 0.1. wanna see what's it? {diff}")
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f" difference is more than Oveerfitting threshold {self.model_trainer_config.overfitting_threshold}")
            #save the model

            logging.info(f"Now save the model")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            logging.info("The artifact is being saved")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)             
            logging.info("The artifact is ready")
            return model_trainer_artifact


        except Exception as e:
            raise SensorException(e,sys)

    