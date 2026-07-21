# TODO: clean this up

# 1. Build stage to install dependencies
FROM python:3.14.6-slim AS python314-dev-base
# Add any extra base packages below. Comment why they're added for your own 
# sanity later. Add any App specific packages further down (there's a comment).
# - `curl` needed to install `pdm`
# - `zsh` for development env
RUN apt-get update && apt-get install -y curl zsh \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# 2. Final runtime stage with font support
FROM python314-dev-base AS eggtimer
ENV IN_CONTAINER=true \
  PYTHONUNBUFFERED=1
# Install fontconfig and fonts (e.g., DejaVu and Microsoft core fonts)
# RUN apk add --no-cache --update \
#     fontconfig \
#     fonts-dejavu \
#     fonts-liberation \
#     fonts-freefont-ttf \
#   && fc-cache -fv

# Copy installed packages from builder
# COPY --from=builder /root/.local /root/.local

# Create a group and user
ARG APP_DIR
ARG APP_GID
ARG APP_GROUP
ARG APP_UID
ARG APP_USER
RUN addgroup --gid "$APP_GID" "$APP_GROUP" \
  && adduser --uid "$APP_UID" --ingroup "$APP_GROUP" --disabled-password --home "/home/$APP_USER" "$APP_USER"
# - `tk` for the `libtk8.6.so` lib for tkinter rendering
# - `alsa-utils mpg123 pipewire-alsa` allows for audio passthrough
#   - `alsa-utils`: Installs `aplay`, which `playsound3` explicitly searches for on Linux to execute audio processing.
#   - `mpg123`: Installs the command-line decoder needed if scripts plays `.mp3` files.
#   - `pipewire-alsa`: This is the crucial bridge. It intercepts standard ALSA audio calls made by aplay inside the container and transparently re-routes them directly out to your host machine's PipeWire daemon.
# - `dbus dbus-x11 libnotify-bin python3-dbus python3-gi` allows for notifications passthrough
RUN apt-get update && apt-get install -y \
  tk \
  alsa-utils mpg123 pipewire-alsa \
  dbus dbus-x11 libnotify-bin python3-dbus python3-gi \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
# Set up a usable terminal experience for development
COPY ./.docker/.zshrc "/home/$APP_USER/"
COPY ./.docker/zsh-autosuggestions.zsh "/home/$APP_USER/"
RUN mkdir -p "$APP_DIR" && chown -R $APP_USER:$APP_GROUP "/home/$APP_USER"*
WORKDIR "$APP_DIR"
# Change to non-root user
USER $APP_USER
# Get pdm versions from: https://github.com/pdm-project/pdm/releases
RUN curl -sSL https://pdm-project.org/install.sh | bash -s -- -v 2.28.0
# COPY ./requirements.txt .
# RUN pip install --target "$APP_DIR/python_modules" -r ./requirements.txt

# CMD ["python", "main.py"]
