#!/bin/bash

set -e

echo "Обновление списка пакетов..."
sudo apt update -y

if ! command -v google-chrome &> /dev/null; then
    echo "Google Chrome не найден, выполняем установку..."
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install -y ./google-chrome-stable_current_amd64.deb
    rm google-chrome-stable_current_amd64.deb
else
    echo "Google Chrome уже установлен. Пропускаем установку."
fi

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
DIRS=("states" "media" "creds")

echo "Создание рабочих директорий..."
for dir in "${DIRS[@]}"; do
    mkdir -p "$SCRIPT_DIR/$dir"
done

echo "Создание и активация виртуального окружения..."
python3 -m venv "$SCRIPT_DIR/.venv"
source "$SCRIPT_DIR/.venv/bin/activate"

echo "Установка зависимостей из requirements.txt..."
pip install -r "$SCRIPT_DIR/requirements.txt"

echo "Деактивация виртуального окружения..."
deactivate

echo "Подготовка завершена успешно!"
