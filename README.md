# GOO Bridge

Cross-platform GUI and CLI for GOO-style NPR rendering with local or remote
headless Blender 5.2.

GOO Bridge is an *external* companion to Blender: it does not modify Blender
and does not redistribute it. It analyzes a `.blend`, stages the scene and its
assets, runs Blender locally or on a server over SSH, verifies the returned
files, and reports which GOO features can be approximated at L2, L1 or L0.

[![build](https://github.com/Toobe53/goo-bridge/actions/workflows/build.yml/badge.svg)](https://github.com/Toobe53/goo-bridge/actions/workflows/build.yml)

**New here?** Start with the bilingual [user tutorial](docs/tutorial.md).

## Status

- 39-item compatibility report: **13 L2**, **15 L1**, **11 L0**
- Local rendering, remote SSH rendering, asset staging and SHA-256 verification
- Tkinter GUI and CLI, Python standard library only
- Tests run on Windows, Linux and macOS; Blender 5.2.3 in CI

L2 means within the agreed 1%–2% visual tolerance. L1 is a deliberate
approximation. L0 is explicitly unsupported and never presented as working.

## Install

```bash
git clone https://github.com/Toobe53/goo-bridge.git
cd goo-bridge
python -m pip install .
goo-bridge doctor
```

Or install the published wheel:

```bash
python -m pip install https://github.com/Toobe53/goo-bridge/releases/download/v0.1.0/goo_bridge-0.1.0-py3-none-any.whl
goo-bridge doctor
```

Requires Python 3.11+ and Blender 5.2.x. Set `GOO_BRIDGE_BLENDER` if Blender is
not in a default location:

```powershell
$env:GOO_BRIDGE_BLENDER = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
```

```bash
export GOO_BRIDGE_BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
```

## Quick start

```bash
goo-bridge analyze scene.blend -o analysis.json
goo-bridge report analysis.json -o analysis.html
goo-bridge render scene.blend -o renders/ --camera Camera --samples 32 --resolution 100
goo-bridge gui
```

### Remote render over SSH

```bash
goo-bridge remote add studio --host 10.0.0.5 --user render --key ~/.ssh/id_ed25519
goo-bridge remote test --profile studio
goo-bridge remote render --profile studio scene.blend -o renders/
```

The remote machine only needs SSH access, Blender 5.2.x and a writable
`~/.goo-bridge`. Passwords are never stored; only SSH keys and the system
`known_hosts` are used. Missing assets block a remote job by default.

## CLI

| Command | Purpose |
|---|---|
| `goo-bridge doctor` | Check Python, Blender, config and engine detection |
| `goo-bridge analyze` | Analyze a `.blend` for GOO groups, assets and settings |
| `goo-bridge report` | Render an HTML analysis report |
| `goo-bridge compat` | Generate the 39-item L2/L1/L0 report |
| `goo-bridge render` | Render locally with Blender 5.2 |
| `goo-bridge gui` | Open the desktop GUI |
| `goo-bridge remote` | Add/test/render/status/fetch/clean over SSH |
| `goo-bridge verify` | Verify a release `SHA256SUMS` directory |

Use `--json` on any command for machine-readable output. Run
`goo-bridge <command> --help` for the exact options.

## Documentation

- [User tutorial](docs/tutorial.md) — install, local and remote workflows
- [Architecture](docs/architecture.md) — components, transport and security
- [Compatibility matrix](docs/compatibility.md) — all 39 items and levels
- [Remote rendering](docs/remote.md) — server setup and troubleshooting
- [CLI reference](docs/cli.md) — every command and option
- [Verification](docs/verification.md) — tests, CI matrix and release checks

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python tools/install_blender.py --dest .blender --json
```

The test suite skips Blender-dependent tests when Blender is not available.
CI runs the same tests on Windows, Linux and macOS, plus a Blender integration
job.

## Security

- No passwords at rest; key-based SSH only
- Remote jobs execute a fixed worker script, not arbitrary shell
- Workspace-relative paths are validated; `..` escapes are rejected
- Downloaded results are SHA-256 checked
- Missing assets are reported and block remote jobs by default

## License

GPL-3.0-or-later. Blender itself is not part of this distribution. GOO Engine
is a separate project; see its own license and the compatibility notes.
