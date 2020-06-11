#
# Copyright 2019-2020 Lukas Schmelzeisen
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
#

from logging import Formatter
from typing import Mapping, Optional

class ColoredFormatter(Formatter):
    log_colors: Mapping[str, str]
    secondary_log_colors: Optional[Mapping[str, Mapping[str, str]]]
    reset: bool
    def __init__(
        self,
        fmt: Optional[str] = ...,
        datefmt: Optional[str] = ...,
        style: str = ...,
        log_colors: Optional[Mapping[str, str]] = ...,
        reset: bool = ...,
        secondary_log_colors: Optional[Mapping[str, Mapping[str, str]]] = ...,
    ): ...
    def color(self, log_colors: Mapping[str, str], level_name: str) -> str: ...

default_log_colors: Mapping[str, str] = ...
escape_codes: Mapping[str, str] = ...
