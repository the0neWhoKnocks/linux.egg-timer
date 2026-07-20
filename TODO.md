Segmentation Fault: g_type_check_instance_is_a () from /lib/x86_64-linux-gnu/libgobject-2.0.so.0

https://www.reddit.com/r/learnpython/comments/1md4hyj/i_think_i_have_to_admit_im_confused_by_how_to/


https://docs.python.org/3/library/tkinter.ttk.html
https://www.geeksforgeeks.org/python/tkinter-cheat-sheet/
https://tkdocs.com/pyref/ttk_frame.html

https://www.geeksforgeeks.org/python/managing-python-dependencies/
https://dev.to/devvspaces/dynamically-managing-dependencies-in-your-python-projects-4pai
https://pypi.org/project/pyinstaller/
  - https://m.youtube.com/watch?v=QWqxRchawZY
https://medium.com/@me.mdhamim/a-comprehensive-guide-to-python-threading-advanced-concepts-and-best-practices-9f3aea6f0a63
- https://github.com/alarm-clock-applet/alarm-clock/tree/master
- https://www.fosslinux.com/107124/installing-and-configuring-python-in-linux-mint.htm
- UV https://m.youtube.com/watch?v=AMdG7IjgSPM
- Ruff https://m.youtube.com/watch?v=828S-DMQog8
- TKinter
  - https://m.youtube.com/watch?v=epDKamC-V-8
  - https://m.youtube.com/watch?v=X5yyKZpZ4vU
- stop watch
  - https://m.youtube.com/watch?v=lADXh_v6ty4
  - https://m.youtube.com/watch?v=mdfuJPGLhPM
  - https://m.youtube.com/watch?v=QBYUws70A7M
  - https://m.youtube.com/watch?v=On8dNuKo4Dw
  - https://m.youtube.com/watch?v=UKs0xhxSOg0


https://popcar.bearblog.dev/using-godot-for-gui-app-development/
https://docs.godotengine.org/en/stable/tutorials/ui/creating_applications.html




uv installs Python by fetching pre-built binaries from python-build-standalone. Because these pre-built Linux distributions lack libXft support—the library responsible for anti-aliasing and font rendering in Tkinter/GUI apps—rendering can appear jagged. To get proper font support, you must use your system's compiled Python version rather than uv's managed standalone versions.
