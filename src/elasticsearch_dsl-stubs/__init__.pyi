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

from datetime import date, datetime
from typing import Generic, Iterator
from typing import Mapping as TMapping
from typing import (
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from elasticsearch import Elasticsearch

_T_JsonMap = TMapping[str, object]
_T_MutableJsonMap = MutableMapping[str, object]
_T_Using = Union[None, str, Elasticsearch]

class connections:  # noqa: N801
    @classmethod
    def create_connection(
        cls,
        alias: str = ...,
        # Parameters from elasticsearch.Transport:
        hosts: Union[
            str, TMapping[str, object], Sequence[Union[str, TMapping[str, object]]]
        ] = ...,
        # connection_class
        # connection_pool_class
        # host_info_callback
        sniff_on_start: bool = ...,
        sniffer_timeout: Optional[float] = ...,
        sniff_timeout: float = ...,
        sniff_on_connection_fail: bool = ...,
        # serializers
        default_minetype: str = ...,
        max_retries: int = ...,
        retry_on_status: Sequence[int] = ...,
        retry_on_timeout: bool = ...,
        send_get_body_as: str = ...,
        # Parameters from elasticsearch.Connection:
        host: str = ...,
        port: int = ...,
        scheme: str = ...,
        use_ssl: bool = ...,
        url_prefix: Optional[str] = ...,
        timeout: float = ...,
        # headers
        http_compress: Optional[bool] = ...,
        cloud_id: Optional[str] = ...,
        api_key: Union[None, str, Sequence[str]] = ...,
        opaque_id: Optional[str] = ...,
        # Parameters from elasticsearch.Urllib3HttpConnection:
        http_auth: Union[str, Tuple[str, str]] = ...,
        verify_certs: bool = ...,
        ssl_show_warn: bool = ...,
        ca_certs: Optional[str] = ...,
        client_certs: Optional[str] = ...,
        client_key: Optional[str] = ...,
        ssl_version: Optional[str] = ...,
        ssl_assert_hostname: Optional[str] = ...,
        ssl_assert_fingerprint: Optional[bool] = ...,
        maxsize: int = ...,
    ) -> Elasticsearch: ...
    @classmethod
    def get_connection(cls, alias: str = ...) -> Elasticsearch: ...

class char_filter:  # noqa: N801
    def __init__(self, name: str): ...

class tokenizer:  # noqa: N801
    def __init__(self, name: str): ...

class token_filter:  # noqa: N801
    def __init__(
        self,
        name: str,
        type: str = ...,  # noqa: A002
        language: str = ...,
        stopwords: str = ...,
    ): ...

class analyzer:  # noqa: N801
    def __init__(
        self,
        name: str,
        *,
        char_filter: Sequence[Union[str, char_filter]] = ...,
        tokenizer: Union[str, tokenizer] = ...,
        filter: Sequence[Union[str, token_filter]] = ...,  # noqa: A002
    ): ...

class IndexTemplate:
    def save(self, using: _T_Using = ...) -> _T_JsonMap: ...

class Index:
    _name: str
    _doc_types: MutableSequence[Type["Document"]]
    def __init__(self, name: str, using: _T_Using = ...): ...
    def create(self, using: _T_Using = ...) -> _T_JsonMap: ...
    def delete(self, using: _T_Using = ...) -> _T_JsonMap: ...
    def delete_alias(self, name: str, using: _T_Using = ...) -> _T_JsonMap: ...
    def exists(self, using: _T_Using = ...) -> bool: ...
    def exists_alias(self, name: str, using: _T_Using = ...) -> bool: ...
    def get_mapping(self, using: _T_Using = ...) -> _T_JsonMap: ...
    def put_alias(self, name: str, using: _T_Using = ...) -> _T_JsonMap: ...
    def refresh(self, using: _T_Using = ...) -> _T_JsonMap: ...
    def as_template(
        self, template_name: str, pattern: str = ..., order: int = ...
    ) -> IndexTemplate: ...
    def settings(self, **kwargs: TMapping[str, object]) -> "Index": ...

class Field:
    def __init__(
        self,
        *,
        multi: bool = ...,
        required: bool = ...,
        doc_values: bool = ...,
        index: bool = ...,
    ): ...

class Boolean(Field): ...
class Short(Field): ...
class Integer(Field): ...
class Long(Field): ...
class Float(Field): ...
class Keyword(Field): ...

class Date(Field):
    def _deserialize(self, data: object) -> Union[datetime, date]: ...

class Text(Field):
    def __init__(
        self,
        *,
        multi: bool = ...,
        required: bool = ...,
        index_options: Optional[str] = ...,
        index_phrases: bool = ...,
        analyzer: Union[None, str, analyzer] = ...,
        fields: Optional[TMapping[str, Text]] = ...,
        term_vector: Optional[str] = ...,
    ): ...

class Object(Field):
    _doc_class: Type["InnerDoc"]
    def __init__(
        self,
        doc_class: Optional[Type["InnerDoc"]] = ...,
        dynamic: Union[None, bool, str] = ...,
        properties: Optional[TMapping[str, object]] = ...,
        *,
        multi: bool = ...,
        required: bool = ...,
    ): ...

class Nested(Object): ...

class Mapping:
    def __getitem__(self, name: str) -> Field: ...
    def __iter__(self) -> Iterator[str]: ...

class DocumentOptions:
    mapping: Mapping

class InnerDoc:
    _doc_type: DocumentOptions

class _DocumentMeta:
    id: str
    index: str
    score: float

_T_Index = Union[None, str, Index]
_T_Document = TypeVar("_T_Document", bound="Document")

class Document:
    _doc_type: DocumentOptions
    _index: Index
    meta: _DocumentMeta
    def __init__(self, *args: object, **kwargs: object): ...
    @classmethod
    def init(cls, index: Union[str, Index], using: _T_Using = ...) -> None: ...
    @classmethod
    def _matches(cls, hit: _T_JsonMap) -> bool: ...
    @classmethod
    def from_es(cls: Type[_T_Document], hit: _T_JsonMap) -> _T_Document: ...
    @classmethod
    def search(
        cls: Type[_T_Document],
        using: _T_Using = ...,
        index: _T_Index = ...,
    ) -> Search[_T_Document]: ...
    def full_clean(self) -> None: ...
    def save(
        self,
        validate: bool = ...,
        skip_empty: bool = ...,
        using: _T_Using = ...,
        index: _T_Index = ...,
    ) -> str: ...
    def to_dict(
        self, include_meta: bool = ..., skip_empty: bool = ...
    ) -> _T_MutableJsonMap: ...

class MetaField:
    def __init__(self, *args: object, **kwargs: object): ...

class Search(Generic[_T_Document]):
    def filter(self, *args: object, **kwargs: object) -> Search[_T_Document]: ...
    def query(self, *args: object, **kwargs: object) -> Search[_T_Document]: ...
    def execute(self) -> Sequence[_T_Document]: ...
