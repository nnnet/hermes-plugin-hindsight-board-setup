"""hindsight-board-setup — per-board Hindsight bank + mental-model setup.

Dormant plugin: defines ``init_board_hindsight(board_slug)`` and supporting
helpers, but the call site (post-board-create hook) is currently not
wired up. See README + plugin.yaml for the rationale.

Exposes the functions both as plugin-relative imports and (for backward
compatibility with old call sites that used ``from tools.hindsight_board_setup
import init_board_hindsight``) via ``sys.modules`` registration under the
legacy name. The legacy registration is harmless when nothing imports the
name and lets a future wire-up land without changes here.
"""

from __future__ import annotations

import logging
import sys

from . import hindsight_board_setup as _module

# Legacy alias: код когда-то жил в /opt/hermes/tools/hindsight_board_setup.py
# (overlay COPY). Сохраняем доступность по тому же import-пути на случай
# если upstream-PR на board-hook будет использовать старое имя.
sys.modules.setdefault("tools.hindsight_board_setup", _module)

# Re-export the public surface.
from .hindsight_board_setup import (  # noqa: E402,F401
    init_board_hindsight,
)

logger = logging.getLogger(__name__)
logger.info(
    "hindsight-board-setup: loaded (dormant — awaiting board-create hook "
    "wire-up; legacy alias tools.hindsight_board_setup registered for "
    "compatibility)"
)
