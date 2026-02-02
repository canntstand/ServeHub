#!/bin/bash

set -e

echo "Смена пароля root..."

while ! [ -f /opt/gitlab/etc/gitlab-rails-rc ]
do
    continue
    sleep 10
done

echo -e "${ROOT_PASSWORD}\n${ROOT_PASSWORD}" | gitlab-rake "gitlab:password:reset[root]"

echo "Все готово!"