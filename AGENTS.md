# AGENTS.md

Public repo of Home Assistant blueprints (`github.com/jeeftor/HomeAssistant`).

## Conventions

- Filenames under `blueprints/automation/` and `blueprints/script/` must match the
  deployed filename on the live HA instance — README import badges and the HA-side
  sync both depend on the path. Renaming a file = update README badge URLs +
  `blueprints/sync_manifest.json` in the same commit.
- Blueprints under `blueprints/` mirror what is deployed on the author's live
  Home Assistant (hand-placed at `blueprints/<domain>/<file>` or imported under
  `blueprints/<domain>/jeeftor/<file>`). `blueprints/sync_manifest.json` holds the
  repo→HA path mapping.
- Third-party blueprints imported into the author's HA (EPMatt, SgtBatten, vorion,
  jerelabs, homeassistant builtins) are NOT in this repo and must not be added.

## Sync to HA

See the "Syncing Blueprints to Home Assistant" section of README.md. TL;DR:
edit → commit → push → run `script.sync_blueprints` on HA.

## Validation

- `python3 -c "import yaml; yaml.safe_load(open(F).read())"` per touched file
  (note: `!input` tags fail `safe_load` — substitute first).
- `device`-typed actions (`domain: <x>, type: <y>, device_id:`) cannot take a
  templated device_id — HA validates them eagerly. To fan out a notification to
  multiple devices, loop with `repeat.for_each` and resolve each device's
  `notify.*` entity via `device_entities()` (see climate-alert.yaml).
