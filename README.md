# GOO Bridge

Cross-platform desktop and command-line app for GOO-style NPR rendering with
stock Blender 5.2.  It opens a `.blend`, reports which GOO features are present,
renders locally, or sends the job to a headless Blender server over SSH.

**Status:** 0.1.0 development.  This repository is the standalone bridge; the
node-group engine is [goo-port](https://github.com/Toobe53/goo-port).

## Quick start

```bash
python -m pip install .
goo-bridge doctor
goo-bridge analyze scene.blend -o analysis.html
goo-bridge render scene.blend -o out/ --samples 32
goo-bridge gui
```

Remote:

```bash
goo-bridge remote add studio --host 10.0.0.5 --user render --key ~/.ssh/id_ed25519
goo-bridge remote test studio
goo-bridge remote render studio scene.blend -o out/ --watch
```

## Requirements

- Python 3.11+
- Blender 5.2.x (local or remote)
- Tkinter for the GUI (bundled with the python.org Windows/macOS installers;
  on Linux install `python3-tk`)

## License

GPL-3.0-or-later.  Blender itself is not bundled or modified.
