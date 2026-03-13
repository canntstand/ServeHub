#!/bin/bash

# скрипт для установки пароля и почты для root пользователя, ник пользователя - root
# перед использованием в контейнере лучше немного подождать до инициализации gitlab-ce

set -e

echo "Смена пароля root..."

echo -e "${ROOT_PASSWORD}\n${ROOT_PASSWORD}" | gitlab-rake "gitlab:password:reset[root]"

echo "Смена почты root..."

gitlab-rails runner "
    user = User.find(1);
    user.email = '${ROOT_EMAIL}';
    user.skip_reconfirmation!;
    user.save!
"
echo "Все готово!"
