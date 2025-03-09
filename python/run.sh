#!/bin/bash

readonly DATABASE_NAME="$1"
readonly USERNAME="$2"

check_everything() {
  if [ -z "$DATABASE_NAME" ]; then
    # --- Quit if user provides empty database name --- #
    printf "[ERROR] Database name appears to be empty.\n"
    printf "[ERROR] Database name: %s\n" "$DATABASE_NAME"
    exit 69
  fi

  if [ -z "$USERNAME" ]; then
    printf "[ERROR] Username appears to be empty.\n"
    printf "[ERROR] Username: %s\n" "$USERNAME"
    exit 42
  fi

  # TODO:
  # This seems to try to connect to database, could be security risk? --- #
  if ! psql "$DATABASE_NAME" -c '\q' >/dev/null 2>&1; then
    printf "[WARNING] '%s' doesn't exist.\n" "$DATABASE_NAME"
    echo "[WARNING] Creating a database."
    create_db
  fi

}

create_db() {
  echo "[INFO] You have provided the following:"
  printf " --> DB Name: %s\n --> Username: %s\n" "$DATABASE_NAME" "$USERNAME"
  read -rp "Continue? [y/n]  "

  if [[ ${REPLY,,} =~ ^y(es)?$ ]]; then
    echo "[INFO] Logging."
    echo "[WARNING] This method uses the following command: sudo -u USERNAME."
    # --- Create a database and logout --- #
    sudo -u "$USERNAME" bash -c "createdb '$DATABASE_NAME'"
    echo "[INFO] Database initialization."
  else
    echo "[INFO] Exiting."
    exit 42
  fi
}

main() {
  echo "[INFO] Starting up."
  db_exists=false
  read -rp "[INFO] Should load the database? [y/n]  "
  if [[ ${REPLY,,} =~ ^y(es)?$ ]]; then
    db_exists=true
    check_everything
  fi

  echo "[INFO] Running."
  python3 "./src/main.py" "$DATABASE_NAME" "$USERNAME" $db_exists true
}
main
