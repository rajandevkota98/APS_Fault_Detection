from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str


@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformation_object_path:str
    transformed_train_path:str
    transformated_test_path:str
    label_enocoder_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str
    f1_train_score:float
    f1_test_score:float
    

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved__accuracy:float


@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str
    saved_model_dir:str