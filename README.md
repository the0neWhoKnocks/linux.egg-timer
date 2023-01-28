# Egg Timer

An Egg-Timer App

---

## Development

Just run:
```sh
./dist/app.py
```
If it shows up in your Panel, success!


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

---

## Sources

Python:
- https://python-gtk-3-tutorial.readthedocs.io/en/latest/application.html#example
- https://blog.devgenius.io/how-to-make-a-clock-with-python-7587e107bb5e

Gtk:
- https://docs.gtk.org/gtk3/#classes
- https://docs.gtk.org/gtk3/css-properties.html

XApp:
- https://lazka.github.io/pgi-docs/XApp-1.0/classes.html
