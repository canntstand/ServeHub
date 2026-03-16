# Гайд по установке и настройке проекта
# Пока кратко

1. Скрипты в scripts
2. Git на хосте для синхронизации репозитория с GitLab CE
    1. Создание репозитория в Gitlab CE, желательно с именем ServeHub
    2. git remote set-url --add --push origin http://localhost:8081/root/ServeHub
    3. чтобы весь проект запушился в gitlab ce: git push origin --all
    4. Регистрация Runner в GitLab
    5. Добавление GitLab Runner и копирование токена в .env, после использование файла для настройки runner в контейнере
    6. Создание runner контейнера
    7. Настройка runner с помощью скрипта
    8. Push -> GitLab CE -> GitLab runner -> Выполнение CI должно работать