#!/bin/bash

# скрипт для установки пароля для root пользователя, ник пользователя - root
# перед использованием в контейнере лучше немного подождать до инициализации gitlab-ce

set -e

echo "Смена пароля root..."

echo -e "${ROOT_PASSWORD}\n${ROOT_PASSWORD}" | gitlab-rake "gitlab:password:reset[root]"

echo "Все готово!"
