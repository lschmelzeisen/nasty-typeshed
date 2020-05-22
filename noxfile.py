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

from pathlib import Path

from nox import options, session
from nox.sessions import Session

options.error_on_external_run = True
options.reuse_existing_virtualenvs = True
options.stop_on_first_error = True


@session(python=["3.6", "3.7", "3.8"])
def test(session: Session) -> None:
    packages = sorted(
        p.name
        for p in Path("src").iterdir()
        if not p.name.endswith(".mypy_cache") and not p.name.endswith(".egg-info")
    )
    session.install("-e", ".[test]")
    session.run("mypy", ".")
    session.run("mypy", *(arg for package in packages for arg in ("-p", package)))
