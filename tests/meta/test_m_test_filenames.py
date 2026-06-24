"""
:mod:`tests.meta.test_m_test_filenames` module.

Guardrails for test-module filename conventions.
"""

from __future__ import annotations

import re

from tests.pytest_helpers import PROJECT_ROOT
from tests.pytest_helpers import TESTS_ROOT

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: INTERNAL CONSTANTS =============================================== #


_DUPLICATE_SUFFIX_PATTERN = re.compile(r'\s+\d+\.py$')


# SECTION: TESTS ============================================================ #


def test_python_test_filenames_have_no_spaces_or_numbered_duplicates() -> None:
    """Test that test-related Python filenames avoid duplicate-copy suffixes."""
    offenders = sorted(
        path.relative_to(PROJECT_ROOT).as_posix()
        for path in TESTS_ROOT.rglob('*.py')
        if '__pycache__' not in path.parts
        if ' ' in path.name or _DUPLICATE_SUFFIX_PATTERN.search(path.name) is not None
    )

    assert not offenders, (
        'Found test Python files with unsupported naming patterns:\n- '
        + '\n- '.join(offenders)
    )
