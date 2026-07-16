# Egg Timer

An Egg-Timer App

- [Install](#install)
- [Development](#development)
  - [Run Container](#run-container)
  - [Installing modules](#installing-modules)
  - [Run App (within running container)](#run-app-within-running-container)
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


### Run Container

```sh
source ./bin/repo-funcs.sh
buildcont  # if not already built
startcont
```


### Installing modules

```sh
# First run, install all project modules
uv pip install -t $PYTHONPATH -r pyproject.toml

# Install individual modules
uv pip install -t $PYTHONPATH <MODULE>==<MODULE_VERSION>
```

### Run App (within running container)

```sh
python -m src.eggtimer --loglevel=info
```


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
