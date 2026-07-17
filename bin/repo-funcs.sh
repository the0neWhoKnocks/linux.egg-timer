#!/bin/bash

CONTAINER="eggtimer"
export CONTAINER_HOSTNAME="eggtimer"
export REPO_FUNCS=()

# Wire up the current User so that any files created in development can easily
# be manipulated by the User or during test runs.
# Export to ensure `docker compose` can use'm
export CURR_UID=$(id -u)
export CURR_GID=$(id -g)
export APP_USER="snake"
export APP_DIR="/home/${APP_USER}/app"

REPO_FUNCS+=("buildcont")
function buildcont {
  DOCKER_BUILDKIT=1 dc build --no-cache "${CONTAINER}"
}

REPO_FUNCS+=("startcont")
function startcont {
  # ensure required directories are set up
  mkdir -p ./.ignore
  touch ./.ignore/.zsh_history
  chmod 777 ./.ignore/.zsh_history
  
  
  
  
  # DBUS_PATH=$(echo "${DBUS_SESSION_BUS_ADDRESS}" | sed 's|unix:path=||')
  # display="${DISPLAY}"
  # export VOL_X11='/tmp/.X11-unix:/tmp/.X11-unix:rw'
  # export VOL_DBUS='/run/dbus/system_bus_socket:/run/dbus/system_bus_socket'
  echo;
  echo "[SET] xhost"
  xhost + "local:${CONTAINER_HOSTNAME}"
  
  
  
  
  
  # envPath="./.env"
  # if [ ! -f "${envPath}" ]; then
  #   echo -e "##\n# NOTE: Any new variables should have defaults added in 'repo-funcs.sh'\n##\n" >> "${envPath}"
  #   echo "API_KEY__TMDB=<VAL>" >> "${envPath}"

  #   echo -e "\n The '.env' file wasn't set up, so it was populated with temporary values.\n Any variables with '<VAL>' need to be updated."
  #   return
  # elif grep -q "<VAL>" "${envPath}"; then
  #   echo -e "\n The '.env' file contains variables that need '<VAL>' replaced."
  #   return
  # fi
  
  # boot container
  docker compose up --remove-orphans -d "${CONTAINER}"
  exitCode=$?
  if [ $exitCode -ne 0 ]; then
    echo "[ERROR] Problem starting ${CONTAINER}"
    return $exitCode
  fi
  
  # enter container
  function exitCont { docker compose down; }
  docker compose exec -u "${APP_USER}" -it "${CONTAINER}" zsh && exitCont || exitCont
}

REPO_FUNCS+=("entercont")
function entercont {
  docker compose exec -u "${APP_USER}" -it "${CONTAINER}" zsh
}
