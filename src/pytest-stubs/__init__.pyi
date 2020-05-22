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

from typing import (
    Any,
    Callable,
    ContextManager,
    Iterable,
    NoReturn,
    Optional,
    Pattern,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from _pytest._code import ExceptionInfo

_T_arg = TypeVar("_T_arg")
_T_func = TypeVar("_T_func", bound=Callable[..., Any])
_T_exp = TypeVar("_T_exp", bound=BaseException)

def fixture(
    callable_or_scope: Union[str, Callable[..., Any]] = ...,
    *args: Any,
    scope: str = ...,
    params: Any = ...,
    autouse: bool = ...,
    ids: Iterable[str] = ...,
    name: str = ...,
) -> Callable[[_T_func], _T_func]: ...
def skip(msg: str = ..., *, allow_module_level: bool = ...) -> NoReturn: ...

class mark:  # noqa: N801
    @staticmethod
    def parametrize(
        argnames: str,
        argvalues: Iterable[_T_arg],
        indirect: bool = ...,
        ids: Optional[Union[Iterable[str], Callable[[_T_arg], str]]] = ...,
        scope: Optional[str] = ...,
    ) -> Callable[[_T_func], _T_func]: ...
    @staticmethod
    def requests_cache_disabled(func: _T_func) -> _T_func: ...
    @staticmethod
    def requests_cache_regenerate(func: _T_func) -> _T_func: ...

def raises(  # noqa: F811
    expected_exception: Union[Type[_T_exp], Tuple[Type[_T_exp], ...]],
    *args: Any,
    match: Optional[Union[str, Pattern[Any]]] = ...,
    **kwargs: Any,
) -> ContextManager[ExceptionInfo[_T_exp]]: ...
