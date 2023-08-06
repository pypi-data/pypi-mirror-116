from datetime import datetime
from typing import List, Union
from tim.data_sources.anomaly_detection.anomaly_detection import get_anomaly_detection_job_status
from tim.data_sources.anomaly_detection import create_anomaly_detection_job, execute_anomaly_detection_job, get_anomaly_detection, get_anomaly_detection_logs, get_anomaly_detection_model_results, get_anomaly_detection_table_results, poll_anomaly_detection_status
from pandas import DataFrame
from tim.core.credentials import Credentials
from tim.data_sources.forecast.types import ExecuteResponse, ForecastJobConfiguration, ForecastResultsResponse, ExecuteForecastJobResponse, CreateForecastConfiguration
from tim.data_sources.anomaly_detection.types import AnomalyDetectionJobConfiguration, AnomalyDetectionResultsResponse, CreateAnomalyDetectionConfiguration, ExecuteAnomalyDetectionJobResponse
from tim.data_sources.workspace.types import Workspace
from tim.data_sources.dataset.types import Dataset, DatasetListVersion
from tim.data_sources.dataset import get_dataset, get_datasets, get_dataset_versions, get_dataset_logs, upload_csv, poll_dataset_version_status, UploadDatasetResponse, UploadCSVConfiguration
from tim.data_sources.forecast import create_forecast_job, execute, get_forecast, get_forecast_accuracies_result, get_forecast_logs, get_forecast_model_results, get_forecast_table_results, poll_forecast_status, get_status
from tim.data_sources.use_case import create_use_case, UseCaseConfiguration
from tim.data_sources.workspace import get_workspaces
from tim.types import Status, SortDirection


class Tim:
  __credentials: Credentials

  def __init__(
      self,
      email: str,
      password: str,
      endpoint: str = "https://tim-platform-dev.tangent.works/api/v5",
  ):
    self.__credentials = Credentials(email, password, endpoint)

  def upload_dataset(
      self, dataset: DataFrame, configuration: UploadCSVConfiguration
  ) -> UploadDatasetResponse:
    """Upload a dataset to the TIM repository

        Parameters
        ----------
        dataset: DataFrame
        	The dataset containing time-series data
        configuration: Dict
        	Metadata of the dataset
          Available keys are: timestampFormat, timestampColumn, decimalSeparator, name, description and samplingPeriod
        	The value of samplingPeriod is a Dict containing the keys baseUnit and value

        Returns
        -------
        id: str
        metadata: Dict | None
        	Dict when successful; None when unsuccessful
        logs: list of Dict
        """
    upload_response = upload_csv(self.__credentials, dataset, configuration)
    id = upload_response['id']

    status_result = poll_dataset_version_status(self.__credentials, id, upload_response['version']['id'])

    metadata = None
    if Status(status_result['status']).value != Status.FAILED.value:
      metadata = get_dataset(self.__credentials, id)

    logs = get_dataset_logs(self.__credentials, id)

    return UploadDatasetResponse(id, metadata, logs)

  def create_forecast(self, dataset_id: str, job_configuration: CreateForecastConfiguration) -> str:
    """Create a forecast job in the workspace the dataset is connected to (the default workspace)

    Parameters
    ----------
    dataset_id: str
        The ID of a dataset in the TIM repository
    job_configuration: CreateForecastConfiguration
        TIM Engine model building and forecasting configuration
        Available keys are: name, configuration, data

    Returns
    -------
    id: str
    """
    workspace_id = get_dataset(self.__credentials, dataset_id)['workspace']['id']

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    use_case_configuration = UseCaseConfiguration(
        name=f'Quick Forecast - {dt_string}', workspaceId=workspace_id, datasetId=dataset_id
    )

    created_use_case_id = create_use_case(
        credentials=self.__credentials, configuration=use_case_configuration
    )['id']

    job_configuration_with_use_case_id = ForecastJobConfiguration(
        name=job_configuration['name'],
        useCaseId=created_use_case_id,
        configuration=job_configuration['configuration'],
        data=job_configuration['data'],
    )
    model = create_forecast_job(
        credentials=self.__credentials, job_configuration=job_configuration_with_use_case_id
    )

    return model['id']

  def execute_forecast(self, forecast_job_id: str,
                       wait_to_finish: bool) -> Union[ExecuteForecastJobResponse, ExecuteResponse]:
    """Execute a forecast job

    Parameters
    ----------
    forecast_job_id: str
        The ID of a forecast job to execute
    wait_to_finish: bool
        Wait for all results to be calculated before returning
        If set to False, the function will return once the job has started the execution process

    Returns
    -------
    metadata: Dict | None
      Dict when successful; None when unsuccessful
    model_result: Dict | None
      Dict when successful; None when unsuccessful
    table_result: DataFrame | None
      DataFrame when successful; None when unsuccessful
    accuracies: Dict | None
      Dict when successful; None when unsuccessful
    logs: list of Dict
    """
    executed_response = execute(self.__credentials, forecast_job_id)
    if not wait_to_finish: return executed_response

    status_result = poll_forecast_status(self.__credentials, forecast_job_id)
    metadata = model_result = table_result = accuracies = None

    if Status(status_result['status']).value != Status.FAILED.value:
      metadata = get_forecast(self.__credentials, forecast_job_id)
      model_result = get_forecast_model_results(self.__credentials, forecast_job_id)
      table_result = get_forecast_table_results(self.__credentials, forecast_job_id)
      accuracies = get_forecast_accuracies_result(self.__credentials, forecast_job_id)

    logs = get_forecast_logs(self.__credentials, forecast_job_id)

    return ExecuteForecastJobResponse(metadata, model_result, table_result, accuracies, logs)

  def get_forecast_results(self, forecast_job_id: str) -> ForecastResultsResponse:
    """Retrieve the results of a forecast job

    Parameters
    ----------
    forecast_job_id: str
        The ID of a forecast job

    Returns
    -------
    metadata: Dict | None
      Dict when successful; None when unsuccessful
    model_result: Dict | None
      Dict when successful; None when unsuccessful
    table_result: DataFrame | None
      Dict when successful; None when unsuccessful
    accuracies: Dict | None
      Dict when successful; None when unsuccessful
    logs: list of Dict
    """
    metadata = model_result = table_result = accuracies = None

    status = get_status(self.__credentials, forecast_job_id)

    if Status(status['status']).value != Status.FAILED.value:
      metadata = get_forecast(self.__credentials, forecast_job_id)
      model_result = get_forecast_model_results(self.__credentials, forecast_job_id)
      table_result = get_forecast_table_results(self.__credentials, forecast_job_id)
      accuracies = get_forecast_accuracies_result(self.__credentials, forecast_job_id)

    logs = get_forecast_logs(self.__credentials, forecast_job_id)

    return ForecastResultsResponse(metadata, model_result, table_result, accuracies, logs)

  def create_and_execute_forecast_job(
      self, dataset_id: str, job_configuration: CreateForecastConfiguration, wait_to_finish: bool
  ) -> Union[ExecuteForecastJobResponse, ExecuteResponse]:
    """Create a forecast job in the workspace the dataset is connected to (default workspace) and execute it

    Parameters
    ----------
    dataset_id: str
      The ID of a dataset in the TIM repository
    job_configuration: CreateForecastConfiguration
      TIM Engine model building and forecasting configuration
      Available keys are: name, configuration, data
    wait_to_finish: bool
      Wait for all results to be calculated before returning
      If set to False, the function will return once the job has started the execution process

    Returns
    -------
    metadata: Dict | None
      Dict when successful; None when unsuccessful
    model_result: Dict | None
      Dict when successful; None when unsuccessful
    table_result: DataFrame | None
      DataFrame when successful; None when unsuccessful
    accuracies: Dict | None
      Dict when successful; None when unsuccessful
    logs: list of Dict
    """

    id = self.create_forecast(dataset_id, job_configuration)
    return self.execute_forecast(id, wait_to_finish)

  def create_anomaly_detection(
      self, dataset_id: str, job_configuration: CreateAnomalyDetectionConfiguration
  ) -> str:
    """Create an anomaly detection job in the workspace the dataset is connected to (default workspace)

    Parameters
    ----------
    dataset_id: str
      The ID of a dataset in the TIM repository
    job_configuration: CreateAnomalyDetectionConfiguration
      TIM Engine model building and anomaly detection configuration
      Available keys are: name, configuration, data

    Returns
    -------
    id: str
    """
    workspace_id = get_dataset(self.__credentials, dataset_id)['workspace']['id']

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    use_case_configuration = UseCaseConfiguration(
        name=f'Quick Anomaly Detection - {dt_string}', workspaceId=workspace_id, datasetId=dataset_id
    )

    created_use_case_id = create_use_case(
        credentials=self.__credentials, configuration=use_case_configuration
    )['id']

    job_configuration_with_use_case_id = AnomalyDetectionJobConfiguration(
        name=job_configuration['name'],
        useCaseId=created_use_case_id,
        configuration=job_configuration['configuration'],
        data=job_configuration['data']
    )

    model = create_anomaly_detection_job(
        credentials=self.__credentials, job_configuration=job_configuration_with_use_case_id
    )

    return model['id']

  def execute_anomaly_detection(self, anomaly_detection_job_id: str, wait_to_finish: bool
                               ) -> Union[ExecuteAnomalyDetectionJobResponse, ExecuteResponse]:
    """Execute an anomaly detection job

    Parameters
    ----------
    anomaly_detection_job_id: str
        The ID of an anomaly detection job to execute
    wait_to_finish: bool
        Wait for all results to be calculated before returning
        If set to False, the function will return once the job has started the execution process

    Returns
    -------
    metadata: Dict | None
      Dict when successful; None when unsuccessful
    model_result: Dict | None
      Dict when successful; None when unsuccessful
    table_result: DataFrame | None
      DataFrame when successful; None when unsuccessful
    logs: list of Dict
    """
    executed_response = execute_anomaly_detection_job(self.__credentials, anomaly_detection_job_id)
    if not wait_to_finish: return executed_response

    status = poll_anomaly_detection_status(self.__credentials, anomaly_detection_job_id)
    metadata = model_result = table_result = None

    if Status(status['status']).value != Status.FAILED.value:
      metadata = get_anomaly_detection(self.__credentials, anomaly_detection_job_id)
      model_result = get_anomaly_detection_model_results(self.__credentials, anomaly_detection_job_id)
      table_result = get_anomaly_detection_table_results(self.__credentials, anomaly_detection_job_id)

    logs = get_anomaly_detection_logs(self.__credentials, anomaly_detection_job_id)

    return ExecuteAnomalyDetectionJobResponse(metadata, model_result, table_result, logs)

  def create_and_execute_anomaly_detection(
      self, dataset_id: str, job_configuration: CreateAnomalyDetectionConfiguration, wait_to_finish: bool
  ) -> Union[ExecuteAnomalyDetectionJobResponse, ExecuteResponse]:
    """Create an anomaly detection job in the workspace the dataset is connected to (default workspace) and execute it

    Parameters
    ----------
    dataset_id: str
      The ID of a dataset in the TIM repository
    job_configuration: CreateAnomalyDetectionConfiguration
      TIM Engine model building and anomaly detection configuration
      Available keys are: name, configuration, data
    wait_to_finish: bool
      Wait for all results to be calculated before returning
      If set to False, the function will return once the job has started the execution process

    Returns
    -------
    metadata: Dict | None
      Dict when successful; None when unsuccessful
    model_result: Dict | None
      Dict when successful; None when unsuccessful
    table_result: DataFrame | None
      DataFrame when successful; None when unsuccessful
    logs: list of Dict
    """

    id = self.create_anomaly_detection(dataset_id, job_configuration)
    return self.execute_anomaly_detection(id, wait_to_finish)

  def get_anomaly_detection_job_results(
      self, anomaly_detection_job_id: str
  ) -> AnomalyDetectionResultsResponse:
    """Retrieve the results of an anomaly detection job

    Parameters
    ----------
    anomaly_detection_job_id: str
        The ID of an anomaly detection job

    Returns
    -------
    metadata: Dict | None
      Dict when successful; None when unsuccessful
    model_result: Dict | None
      Dict when successful; None when unsuccessful
    table_result: DataFrame | None
      Dict when successful; None when unsuccessful
    accuracies: Dict | None
      Dict when successful; None when unsuccessful
    logs: list of Dict
    """
    metadata = model_result = table_result = None

    status = get_anomaly_detection_job_status(self.__credentials, anomaly_detection_job_id)

    if Status(status['status']).value != Status.FAILED.value:
      metadata = get_anomaly_detection(self.__credentials, anomaly_detection_job_id)
      model_result = get_anomaly_detection_model_results(self.__credentials, anomaly_detection_job_id)
      table_result = get_anomaly_detection_table_results(self.__credentials, anomaly_detection_job_id)

    logs = get_anomaly_detection_logs(self.__credentials, anomaly_detection_job_id)

    return AnomalyDetectionResultsResponse(metadata, model_result, table_result, logs)

  def get_workspaces(
      self,
      offset: Union[int, None] = None,
      limit: Union[int, None] = None,
      userGroupId: Union[str, None] = None,
      sort: Union[SortDirection, None] = None
  ) -> List[Workspace]:
    """Get a list of Workspaces

    Parameters
    ----------
    offset : Union[int, None], optional
        Number of records to be skipped from beggining of the list, by default None
    limit : Union[int, None], optional
        Maximum number of records to be returned, by default None
    userGroupId : Union[str, None], optional
        User Group ID, by default None
    sort : Union[SortDirection, None], optional
        Sorting output by the chosen attribute. +/- indicates ascending/descending order, by default None
    """
    return get_workspaces(self.__credentials, offset, limit, userGroupId, sort)

  def get_datasets(
      self,
      offset: Union[int, None] = None,
      limit: Union[int, None] = None,
      workspaceId: Union[str, None] = None,
      sort: Union[SortDirection, None] = None
  ) -> List[Dataset]:
    """Get a list of the versions of a Dataset

    Parameters
    ----------
    offset : Union[int, None], optional
        Number of records to be skipped from beggining of the list, by default None
    limit : Union[int, None], optional
        Maximum number of records to be returned, by default None
    """
    return get_datasets(self.__credentials, offset, limit, workspaceId, sort)

  def get_dataset_versions(
      self,
      id: str,
      offset: Union[int, None] = None,
      limit: Union[int, None] = None,
  ) -> List[DatasetListVersion]:
    return get_dataset_versions(self.__credentials, id, offset, limit)

  @property
  def credentials(self):
    return self.__credentials
