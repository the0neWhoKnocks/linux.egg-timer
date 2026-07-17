# 1. Build stage to install dependencies
FROM python:3.14.6-alpine3.23 AS python314-dev-base
# ENV DEBIAN_FRONTEND=noninteractive
# Add any extra base packages below. Comment why they're added for your own 
# sanity later. Add any App specific packages further down (there's a comment).
# - `uv` toolkit for working with python projects/modules
# - `zsh` for development env
# RUN apk add --no-cache --update build-base zsh
RUN apk add --no-cache --update uv zsh
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --user -r requirements.txt

# 2. Final runtime stage with font support
FROM python314-dev-base AS eggtimer
# ENV DEBIAN_FRONTEND=noninteractive \
ENV IN_CONTAINER=true \
  PYTHONUNBUFFERED=1
  # PATH=/root/.local/bin:$PATH
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
# Install tk for the `libtk8.6.so` lib
RUN apk add --no-cache --update tk
# Set up a usable terminal experience for development
COPY ./.docker/.zshrc "/home/$APP_USER/"
COPY ./.docker/zsh-autosuggestions.zsh "/home/$APP_USER/"
RUN mkdir -p "$APP_DIR" && chown -R $APP_USER:$APP_GROUP "/home/$APP_USER"*
WORKDIR "$APP_DIR"
# Change to non-root user
USER $APP_USER
# COPY ./requirements.txt .
# RUN pip install --target "$APP_DIR/python_modules" -r ./requirements.txt

# CMD ["python", "main.py"]




# ## Base Node image
# # NOTE: When updating node version, update in `e2e/.docker/proxied.Dockerfile` as well.
# FROM node:24.1.0-alpine3.22 AS node24-dev-base
# # Add any extra base packages below. Comment why they're added for your own 
# # sanity later. Add any App specific packages further down (there's a comment).
# # - `rsync` for the `dist` setup
# # - `tzdata` so the `TZ` env var works for timezones
# # - `vim zsh` for development env
# RUN apk add --no-cache --update rsync tzdata vim zsh

# # Set up a usable terminal experience for development
# RUN echo "update-notifier=false" >> /home/node/.npmrc
# COPY ./.docker/.vimrc /home/node/.vimrc
# COPY ./.docker/.zshrc /home/node/.zshrc
# COPY ./.docker/zsh-autosuggestions.zsh /home/node/zsh-autosuggestions.zsh

# # start building the base
# FROM node24-dev-base AS tvcal--packagejson
# # Create a temporary package.json where things like `version` and `scripts`
# # are omitted so the cache of the build step won't be invalidated.
# COPY --chown=node:node ./package*.json ./
# RUN ["node", "-e", " \
#   const pkg = JSON.parse(fs.readFileSync('package.json', 'utf-8')); \
#   const lock = JSON.parse(fs.readFileSync('package-lock.json', 'utf-8')); \
#   \
#   let preInstallScript; \
#   if (pkg.scripts && pkg.scripts.preinstall) preInstallScript = pkg.scripts.preinstall; \
#   \
#   delete pkg.devDependencies; \
#   delete pkg.scripts; \
#   delete pkg.version; \
#   delete lock.version; \
#   \
#   if (preInstallScript) pkg.scripts = { preinstall: preInstallScript }; \
#   \
#   fs.writeFileSync('package.json', JSON.stringify(pkg)); \
#   fs.writeFileSync('package-lock.json', JSON.stringify(lock)); \
# "]

# # Env where prod deps are installed
# FROM node24-dev-base AS tvcal--prod
# ENV APP=/home/node/app
# ENV IN_CONTAINER=true
# ENV NODE_ENV=production
# RUN mkdir -p $APP/node_modules && chown -R node:node /home/node/*

# ######
# ## Add App specific packages below
# ######
# # RUN apk add --no-cache --update <PACKAGE> <PACKAGE> ...

# WORKDIR $APP

# # Copy over package related files from the preperation step to install
# # production modules
# COPY --chown=node:node --from=tvcal--packagejson ./package*.json ./

# # Install production dependencies and compile assets
# RUN npm i --only=production --quiet --unsafe-perm \
#   && rm ./package*.json

# # Env with dev deps to compile assets
# FROM tvcal--prod AS tvcal--dev
# # Install Dev deps (updated scripts or deps will invalidate build-cache)
# COPY --chown=node:node ./package*.json ./
# ENV NODE_ENV=development
# RUN npm i --quiet
# # Build is separate to utilize the build-cache if the package.json hasn't changed.
# COPY --chown=node:node ./bin/prep-dist.sh ./bin/
# COPY --chown=node:node ./src ./src
# COPY --chown=node:node ./svelte.config.js ./
# COPY --chown=node:node ./webpack.config.js ./
# RUN npm run build

# # Bring over compiled assets and finalize.
# FROM tvcal--prod AS tvcal
# COPY --chown=node:node --from=tvcal--dev $APP/dist/constants.js ./
# COPY --chown=node:node --from=tvcal--dev $APP/dist/utils ./utils
# COPY --chown=node:node --from=tvcal--dev $APP/dist/server ./server
# COPY --chown=node:node --from=tvcal--dev $APP/dist/public ./public

# # Expose the default port from the Server, on the container
# EXPOSE 3000

# # Start the app
# CMD ["node", "server"]
