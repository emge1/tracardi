from typing import List, Optional

from pydantic import BaseModel
from tracardi.service.plugin.domain.result import Result

from .entity import Entity
from .input_params import InputParams


class DebugInput(BaseModel):
    edge: Optional[Entity] = None
    params: Optional[InputParams] = None


class DebugOutput(BaseModel):
    edge: Optional[Entity] = None
    results: Optional[List[Result]] = None


class Profiler(BaseModel):
    startTime: float
    runTime: float
    endTime: float


class DebugCallInfo(BaseModel):
    profiler: Profiler
    input: DebugInput
    output: DebugOutput
    init: Optional[dict] = None
    profile: Optional[dict] = {}
    event: Optional[dict] = {}
    session: Optional[dict] = {}
    error: Optional[str] = None
    run: bool = False

    def has_error(self):
        return self.error is not None
