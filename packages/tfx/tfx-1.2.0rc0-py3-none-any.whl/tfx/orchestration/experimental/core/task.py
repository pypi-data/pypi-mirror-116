# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Task class and related functionality.

Task instructs the work to be peformed. A task is typically generated by the
core task generation loop based on the state of MLMD db.
"""

import abc
import typing
from typing import Dict, List, Type, TypeVar

import attr
from tfx import types
from tfx.proto.orchestration import pipeline_pb2
from tfx.utils import status as status_lib

from ml_metadata.proto import metadata_store_pb2


@attr.s(auto_attribs=True, frozen=True)
class PipelineUid:
  """Unique identifier for a pipeline.

  Attributes:
    pipeline_id: Id of the pipeline containing the node. Corresponds to
      `Pipeline.pipeline_info.id` in the pipeline IR.
    key: An optional key associated with the pipeline.
  """
  pipeline_id: str
  key: str = ''

  @classmethod
  def from_pipeline(cls: Type['PipelineUid'],
                    pipeline: pipeline_pb2.Pipeline) -> 'PipelineUid':
    return cls(pipeline_id=pipeline.pipeline_info.id)


@attr.s(auto_attribs=True, frozen=True)
class NodeUid:
  """Unique identifier for a node in the pipeline.

  Attributes:
    pipeline_uid: The pipeline UID.
    node_id: Node id. Corresponds to `PipelineNode.node_info.id` in the pipeline
      IR.
  """
  pipeline_uid: PipelineUid
  node_id: str

  @classmethod
  def from_pipeline_node(cls: Type['NodeUid'], pipeline: pipeline_pb2.Pipeline,
                         node: pipeline_pb2.PipelineNode) -> 'NodeUid':
    return cls(
        pipeline_uid=PipelineUid.from_pipeline(pipeline),
        node_id=node.node_info.id)


# Task id can be any hashable type.
TaskId = typing.Hashable

_TaskT = TypeVar('_TaskT', bound='Task')


class Task(abc.ABC):
  """Task instructs the work to be performed."""

  @property
  @abc.abstractmethod
  def task_id(self) -> TaskId:
    """Returns a unique identifier for this task.

    The concrete implementation must ensure that the returned task id is unique
    across all task types.
    """

  @classmethod
  def task_type_id(cls: Type[_TaskT]) -> str:
    """Returns task type id."""
    return cls.__name__


@attr.s(auto_attribs=True, frozen=True)
class ExecNodeTask(Task):
  """Task to instruct execution of a node in the pipeline.

  Attributes:
    node_uid: Uid of the node to be executed.
    execution_id: Id of the MLMD execution associated with the current node.
    contexts: List of contexts associated with the execution.
    exec_properties: Execution properties of the execution.
    input_artifacts: Input artifacts dict.
    output_artifacts: Output artifacts dict.
    executor_output_uri: URI for the executor output.
    stateful_working_dir: Working directory for the node execution.
    pipeline: The pipeline IR proto containing the node to be executed.
    is_cancelled: Indicates whether this is a cancelled execution. The task
      scheduler is expected to gracefully exit after doing any necessary
      cleanup.
  """
  node_uid: NodeUid
  execution_id: int
  contexts: List[metadata_store_pb2.Context]
  exec_properties: Dict[str, types.Property]
  input_artifacts: Dict[str, List[types.Artifact]]
  output_artifacts: Dict[str, List[types.Artifact]]
  executor_output_uri: str
  stateful_working_dir: str
  pipeline: pipeline_pb2.Pipeline
  is_cancelled: bool = False

  @property
  def task_id(self) -> TaskId:
    return _exec_node_task_id(self.task_type_id(), self.node_uid)

  def get_pipeline_node(self) -> pipeline_pb2.PipelineNode:
    for node in self.pipeline.nodes:
      if node.pipeline_node.node_info.id == self.node_uid.node_id:
        return node.pipeline_node
    raise ValueError(
        f'Node not found in pipeline IR; node uid: {self.node_uid}')


@attr.s(auto_attribs=True, frozen=True)
class CancelNodeTask(Task):
  """Task to instruct cancellation of an ongoing node execution."""
  node_uid: NodeUid

  @property
  def task_id(self) -> TaskId:
    return (self.task_type_id(), self.node_uid)


@attr.s(auto_attribs=True, frozen=True)
class FinalizePipelineTask(Task):
  """Task to instruct finalizing a pipeline run."""
  pipeline_uid: PipelineUid
  status: status_lib.Status

  @property
  def task_id(self) -> TaskId:
    return (self.task_type_id(), self.pipeline_uid)


@attr.s(auto_attribs=True, frozen=True)
class FinalizeNodeTask(Task):
  """Task to instruct finalizing a node execution."""
  node_uid: NodeUid
  status: status_lib.Status

  @property
  def task_id(self) -> TaskId:
    return (self.task_type_id(), self.node_uid)


def is_exec_node_task(task: Task) -> bool:
  return task.task_type_id() == ExecNodeTask.task_type_id()


def is_cancel_node_task(task: Task) -> bool:
  return task.task_type_id() == CancelNodeTask.task_type_id()


def is_finalize_pipeline_task(task: Task) -> bool:
  return task.task_type_id() == FinalizePipelineTask.task_type_id()


def is_finalize_node_task(task: Task) -> bool:
  return task.task_type_id() == FinalizeNodeTask.task_type_id()


def exec_node_task_id_from_pipeline_node(
    pipeline: pipeline_pb2.Pipeline, node: pipeline_pb2.PipelineNode) -> TaskId:
  """Returns task id of an `ExecNodeTask` from pipeline and node."""
  return _exec_node_task_id(ExecNodeTask.task_type_id(),
                            NodeUid.from_pipeline_node(pipeline, node))


def _exec_node_task_id(task_type_id: str, node_uid: NodeUid) -> TaskId:
  return (task_type_id, node_uid)
