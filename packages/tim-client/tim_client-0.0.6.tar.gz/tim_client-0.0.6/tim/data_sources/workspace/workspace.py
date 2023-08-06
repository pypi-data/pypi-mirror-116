from tim.core.credentials import Credentials
from tim.core.api import execute_request
from tim.types import SortDirection
from .types import WorkspaceListPayload, Workspace
from typing import List, Union


def get_workspaces(
    credentials: Credentials,
    offset: Union[int, None] = None,
    limit: Union[int, None] = None,
    userGroupId: Union[str, None] = None,
    sort: Union[SortDirection, None] = None
) -> List[Workspace]:
  payload = WorkspaceListPayload()
  if offset: payload['offset'] = offset
  if limit: payload['limit'] = limit
  if userGroupId: payload['userGroupId'] = userGroupId
  if sort: payload['sort'] = sort

  return execute_request(credentials=credentials, method='get', path='/workspaces', body=payload)
