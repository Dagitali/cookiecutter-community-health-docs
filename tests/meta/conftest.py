"""
:mod:`tests.meta.conftest` module.

Shared fixtures and helpers for pytest-based meta tests.
"""

from __future__ import annotations

import pytest

# SECTION: MARKERS ========================================================== #


# Directory-level marker for meta tests.
pytestmark = pytest.mark.meta
