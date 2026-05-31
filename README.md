# hermes-plugin-hindsight-board-setup

External Hermes plugin that provides per-board Hindsight memory bank
setup — meant to be called whenever a new kanban board is created so
the team working on that project has shared mental-model storage.

## Why

When a chief spawns a team for a sub-project (kanban board), two
parallel knowledge stores are populated as work progresses:

| Store | Slice | Read access |
|---|---|---|
| GIT (`workspaces/<board>/`) | **WHAT** was done — commits, file changes, code structure | `git log`, `git diff`, file reads |
| Hindsight bank `hermes-board-<slug>` mental-model `project-overview` | **WHY / WHAT-FOR** — motivation, current goals, decisions + rationale, rejected alternatives, blockers, open questions | `hindsight_recall` |

The split is deliberate: the two are **non-overlapping** so they don't
drift against each other. Hindsight gets the intent layer; git gets the
artefact layer. Together they cover «что нужно знать про этот проект»
without duplication.

## What this plugin does

Provides:

* `init_board_hindsight(board_slug)` — main entry point. Creates the
  bank if missing, then ensures the `project-overview` mental-model is
  initialised with a seed prompt.
* `_ensure_bank(bank_id, *, board_slug)` — idempotent bank creation
* `_ensure_project_overview(bank_id, board_slug)` — idempotent
  mental-model creation
* Plus low-level HTTP helpers (`_http_json`, `_api_url`)

## Status: DORMANT

The plugin **loads** but is not currently called. The historical call
site was in our overlay's `hermes_cli/kanban_db.py:_maybe_init_github_mirror`
which we dropped 2026-05-31 when migrating image build to upstream
release tag `v2026.5.29.2`. That tag's `kanban_db.py` does not contain
the hook.

To re-activate, one of:

1. **Upstream PR** — add a post-board-create hook in
   `hermes_cli/kanban_db.py` that emits an event a plugin can subscribe
   to. Land our hook in this plugin's `__init__.py`.

2. **Monkey-patch plugin** — wrap `KanbanDB.create_board()` at this
   plugin's load time and call `init_board_hindsight(board.slug)` on
   success. Direct, fragile if upstream renames the method, but works
   today without upstream cooperation.

## Configuration

The plugin reads:

* `HINDSIGHT_URL` (default `http://127.0.0.1:8888`) — base URL of the
  Hindsight service (typically `hermes-hindsight` sidecar)

## Use

```yaml
# config.yaml
plugins:
  enabled:
    - hindsight-board-setup
```

The plugin will load and log:

```
INFO hindsight-board-setup: loaded (dormant — awaiting board-create
hook wire-up; legacy alias tools.hindsight_board_setup registered for
compatibility)
```

When wire-up lands, it will activate per-board on each
`KanbanDB.create_board()` call.

## Mounting

```yaml
# docker-compose.hermes-core.yml — inherited via sources/hermes-plugins-collection mount
volumes:
  - ./sources/hermes-plugins-collection/hindsight-board-setup:/opt/data/plugins/hindsight-board-setup:ro
```

(or wrapped into the collection super-repo mount that already covers
all sibling plugins).
