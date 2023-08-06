from typing_extensions import TypedDict
from tim.types import ObjId, SortDirection


class Workspace(TypedDict):
  id: str
  name: str
  description: str
  userGroup: ObjId
  isFavorite: bool
  createdAt: str
  createdBy: str
  updatedAt: str
  updatedBy: str


class WorkspaceListPayload(TypedDict, total=False):
  offset: int
  limit: int
  userGroupId: str
  sort: SortDirection
