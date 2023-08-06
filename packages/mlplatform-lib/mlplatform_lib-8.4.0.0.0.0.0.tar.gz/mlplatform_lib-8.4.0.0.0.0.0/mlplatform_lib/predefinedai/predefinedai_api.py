import json
from mlplatform_lib.api_client import ApiClient, RunMode
from mlplatform_lib.dataclass.experiment.type import ExperimentType
from mlplatform_lib.dataclass.model.type import ModelStatus
from mlplatform_lib.dataclass.model import ModelPredefinedaiDto
from mlplatform_lib.mlplatform.mlplatform_http_client import MlPlatformUserAuth
from mlplatform_lib.predefinedai.predefinedai_http_client import PredefinedAIHttpClient
import os
from typing import Dict, List, Optional


class PredefinedAIApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        if api_client.run_mode == RunMode.KUBERNETES:
            self.predefinedai_client = PredefinedAIHttpClient(mlplatform_addr=os.environ["mlplatformAddr"])
            self.mlplatform_auth = MlPlatformUserAuth(
                project_id=self.api_client.projectId,
                user_id=self.api_client.userId,
                authorization=self.api_client.Authorization,
                authorization_type=self.api_client.authorizationType,
            )
        self.experiment_id = self.api_client.experiment_id
        self.train_id = self.api_client.train_id

    def get_model_infos(self) -> Optional[List[ModelPredefinedaiDto]]:
        if self.api_client == RunMode.KUBERNETES:
            return self.predefinedai_client.get_model_infos(
                experiment_id=self.api_client.experiment_id,
                train_id=self.api_client.train_id,
                auth=self.mlplatform_auth,
            )
        else:
            print("Current mode is local, Skip get_model_infos.")
            return None

    def insert_model_info(
        self,
        model_name: str,
        description: str,
        algorithm: str,
        metric: str,
        metric_result: str,
        model_path: str,
        model_json: Dict,
    ) -> Optional[ModelPredefinedaiDto]:
        if self.api_client == RunMode.KUBERNETES:
            model_predefinedai_dto = ModelPredefinedaiDto(
                id=0,
                train_id=self.train_id,
                name=model_name,
                experiment_type=ExperimentType.PREDEFINEDAI.value,
                description=description,
                algorithm=algorithm,
                metric=metric,
                metric_result=metric_result,
                model_path=model_path,
                model_json=json.dumps(model_json),
                status=ModelStatus.SUCCESS.value,
            )
            return self.predefinedai_client.insert_model_info(
                experiment_id=self.experiment_id,
                train_id=self.train_id,
                dto=model_predefinedai_dto,
                auth=self.mlplatform_auth,
            )
        else:
            print("Current mode is local, Skip insert_model_info.")
            return ModelPredefinedaiDto(
                id=1,
                train_id=self.train_id,
                name=model_name,
                experiment_type=ExperimentType.PREDEFINEDAI.value,
                description=description,
                algorithm=algorithm,
                metric=metric,
                metric_result=metric_result,
                model_path=model_path,
                model_json=json.dumps(model_json),
                status=ModelStatus.SUCCESS.value,
            )

    def insert_visualizations(self, model_id: int, type: str, result: str) -> None:
        if self.api_client == RunMode.KUBERNETES:
            pass
        else:
            print("Current mode is local, Skip insert_visualizations.")

    def upload_inference_csv(self, inference_csv_path: str):
        if self.api_client == RunMode.KUBERNETES:
            self.predefinedai_client.upload_inference_csv(
                experiment_id=self.experiment_id,
                inference_id=self.inference_id,
                inference_csv_path=inference_csv_path,
                auth=self.mlplatform_auth,
            )
            os.remove(inference_csv_path)
        else:
            print("Current mode is local, Skip upload_inference_csv.")
