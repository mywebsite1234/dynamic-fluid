"""Runtime license-acceptance gate for dynamic_fluid.

dynamic-fluid is distributed under the MIT License with the Commons Clause
(see the LICENSE file): free to use and modify, but it may not be sold, and
any use must credit Danylo Stoian. `pip install` itself can't prompt for and
enforce agreement (it just unpacks a wheel, often in non-interactive CI/
build contexts), so acceptance is instead enforced the first time the
package is actually imported or run.
"""

import os
import sys
from pathlib import Path

_ENV_VAR = "DYNAMIC_FLUID_ACCEPT_LICENSE"
_MARKER_FILE = Path.home() / ".dynamic_fluid" / "license_accepted"

_NOTICE = """
dynamic-fluid is licensed under the MIT License with the Commons Clause:
  - You may use, modify, and distribute this software, including inside
    commercial projects.
  - You may NOT sell dynamic-fluid itself, or a product/service whose value
    derives substantially from it.
  - Any use must clearly credit Danylo Stoian as the original author.

Full text: {license_path}
"""


def _license_path() -> str:
    candidates = [
        Path(__file__).resolve().parent / "LICENSE",
        Path(__file__).resolve().parent.parent / "LICENSE",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return "https://github.com/your-username/dynamic-fluid/blob/main/LICENSE"


def _is_truthy(value: str) -> bool:
    return value.strip().lower() in ("1", "true", "yes", "y")


def _write_marker() -> None:
    try:
        _MARKER_FILE.parent.mkdir(parents=True, exist_ok=True)
        _MARKER_FILE.write_text("accepted\n")
    except OSError:
        pass


def ensure_license_accepted() -> None:
    """Make sure the user has accepted the license, prompting if needed.

    Acceptance is remembered in ``~/.dynamic_fluid/license_accepted`` so
    this only prompts once per machine/user. In non-interactive contexts
    (CI, scripts with no attached terminal) set
    ``DYNAMIC_FLUID_ACCEPT_LICENSE=1`` to accept without a prompt.
    """
    if _MARKER_FILE.exists():
        return

    if _is_truthy(os.environ.get(_ENV_VAR, "")):
        _write_marker()
        return

    notice = _NOTICE.format(license_path=_license_path())

    if not sys.stdin.isatty():
        raise SystemExit(
            "dynamic-fluid: license not yet accepted, and no terminal is "
            f"attached to prompt for it.\n{notice}\n"
            f"To accept non-interactively (e.g. in CI), set {_ENV_VAR}=1 "
            "before importing dynamic_fluid."
        )

    print(notice)
    try:
        answer = input("Type 'I AGREE' to accept and continue: ")
    except (EOFError, KeyboardInterrupt):
        answer = ""

    if answer.strip().upper() != "I AGREE":
        raise SystemExit("dynamic-fluid: license not accepted. Exiting.")

    _write_marker()
