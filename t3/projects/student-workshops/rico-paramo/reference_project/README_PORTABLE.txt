PORTABLE PYTHON VISUAL SHOW
===========================

Run:
1. Keep PortableVisualShow.exe, config.json and launch.bat in the same folder.
2. Double-click launch.bat.
3. Press F to toggle FPS display.
4. Press ESC to exit.

Live defense:
- Change orbit_speed or particle_count in config.json.
- Save.
- Relaunch.
- Explain the predicted visual change.

The build is designed for manual launch. It does not use USB autorun or hidden startup behavior.
Verification added 2026-10-14:
  PortableVisualShow.exe --verify
Renders ten headless frames, prints PASS plus the effective config, and exits.
This verifies packaging/configuration; it does not replace a visible USB/offline demo.
config.json must remain beside the executable. Move both files together.
Invalid numeric fields fall back individually; sizes and particle counts are bounded.
Build environment verified: Python 3.12, pygame 2.6.1, PyInstaller 6.16.0.
