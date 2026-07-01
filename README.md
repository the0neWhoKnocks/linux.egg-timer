# Egg Timer

An Egg-Timer App

- [Install](#install)
- [Development](#development)
  - [Setup](#setup)
  - [Run](#run)
  - [Gtk Inspector](#gtk-inspector)
  - [Sound Creation](#sound-creation)
  - [Thread Check](#thread-check)
  - [Debug](#debug)
- [Sources](#sources)

---

## Install

Run:
```sh
./install.sh
```

If the egg icon doesn't appear in the panel, run `tail -f ~/.xsession-errors` to see if there were any errors.

---

## Development

```sh
cd ./src
uv run python -m eggtimer --loglevel=info
```

### Setup

1. Install `uv` (if not already installed): https://docs.astral.sh/uv/getting-started/installation/
1. Initialize (if not already initialized): `uv init [--python <VERSION>]`
    - If you need to change the Python version: `uv python pin <VERSION>`
1. Install a specific version of Python: `uv python install <VERSION>`
1. Install listed deps (pyproject.toml or requirements.txt): `uv sync`
1. Deps:
    ```sh
    uv (add/remove) <PACKAGE> <PACKAGE>
    uv (add/remove) --dev <PACKAGE> <PACKAGE>
    
    uv tool (install/uninstall) ruff
    ```
1. `venv`
    ```sh
    # on
    source .venv/bin/activate
    
    # off
    deactivate
    ```
1. Cache
    ```sh
    # print the cache location
    uv cache dir
    
    # clear the cache
    uv cache clean
    ```

sudo apt install libgirepository-2.0-dev


### Run
```sh
./dist/app.py --loglevel=info
```
If it shows up in your Panel, success! Otherwise run `tail -f ~/.xsession-errors` to see if there were any errors.


### Gtk Inspector

To view Gtk component hiearchies and style classes/names, you'll need the `GtkInspector`.

```sh
# If `libgtk-3-dev` isn't installed, do so
sudo apt install libgtk-3-dev

# Enable with
gsettings set org.gtk.Settings.Debug enable-inspector-keybinding true
```

With an App/Window focused, hit `CTRL+SHIFT+I` and it should open with that App's items listed in the Objects view. Click on the lightbulb icon to `Show Details`, then click the drop-down and select `CSS nodes`.


### Sound Creation

I converted a system sound to a `.wav` so Alsa could play it.
```sh
# -ac 1     (convert to mono)
# -ar 8000  (bitrate, roughly 8khz)
ffmpeg -acodec libvorbis -i "/usr/share/sounds/freedesktop/stereo/complete.oga" -ac 1 -ar 8000 "./dist/complete.wav"
```


### Thread Check

To ensure Threads are being torn down:
```sh
# Get the PID from System Monitor.
ps -T -p <PID>

# Count the number of items before you start running a Timer, then after a Timer
# has started. After the Timer has completed, the number of items should reset.
# A new Thread will show up in the CMD column under `<NAME>.py` (NAME being the
# script that started the Thread).
```


### Debug

```sh
# With faulthandler ============================================================

PYTHONFAULTHANDLER=1 python ./dist/app.py --loglevel=info

# With Python Debugger =========================================================

python -m pdb ./dist/app.py --loglevel=info
# type 'continue' to start
# type 'run' to restart

# With GNU Debugger ============================================================

# If `python3-dbg` isn't installed, do so
sudo apt install libglib2.0-0t64-dbgsym python3-dbg

# Start session (*)
gdb python
(gdb) run ./dist/app.py --loglevel=info
# Once the error occurs, start viewing the backtrace
(gdb) bt

# (*) If you get warnings regarding "could not find '.gnu_debugaltlink'", you're likely missing the debug symbols for the specified package. Ubuntu based systems have a Debuginfod server which detects the missing symbols and will fetch them. To enable this, you'd have to change the initial `gdb` command to this:
export DEBUGINFOD_URLS="https://debuginfod.ubuntu.com"; gdb python
```

---

## Sources

Python:
- https://python-gtk-3-tutorial.readthedocs.io/en/latest/application.html#example
- https://blog.devgenius.io/how-to-make-a-clock-with-python-7587e107bb5e

Gdk:
- https://docs.gtk.org/gdk3/index.html#classes

Gtk:
- https://docs.gtk.org/gtk3/#classes
- https://docs.gtk.org/gtk3/css-properties.html

XApp:
- https://lazka.github.io/pgi-docs/XApp-1.0/classes.html
