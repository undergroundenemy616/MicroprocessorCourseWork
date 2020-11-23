# My-HomeCam-Security-Bot
TelegramBot, реализующий клиентскую часть системы контроля входа в умном доме.
<img src = "https://user-images.githubusercontent.com/55200686/99937212-2b40f400-2d76-11eb-84b2-21b46d074307.png" width = "700">

### Демонстрация (видео)

| Регистрация нового человека | Открыли ему дверь |
| ------------- | ------------- |
| [<img src="https://user-images.githubusercontent.com/55200686/99917137-72e86100-2d1f-11eb-9bf9-a548b8d7a699.jpg" width="550">](https://drive.google.com/file/d/1A2cUUTbxGFeNGI3LN1ukyz4THrzo9D6J/view?usp=sharing) | [<img src="https://user-images.githubusercontent.com/55200686/99936928-668ef300-2d75-11eb-89c7-18b69ef0015f.jpg" width="550">](https://drive.google.com/file/d/1H5ayyIAoAmhwgudwDymaXe8MtvTAsokQ/view?usp=sharing)  |

### Клонирование репозитория
 1. Перед запуском перейдите в виртуальное окружение *python* `venv\` и активируйте его.
 2. Далее, так как бот взаимодействует с серверами Telegram через *webhook*, то нужно прокинуть сетевой тунель при помощи команды `ngrok https 8000` и вставить полученный url-адресс в файл `/micro/micro/settings.py` в поле `URL`. 
 3. Затем для асинсхронного выполнения задач необходимо включить *Redis* и *Celery*.
 4. Запускаем бота `python manage.py runserver`.
 
⚡ Система будет работать, пока работает Raspberry Pi.

### Более подробно о системе чистайте в [Report.pdf](https://github.com/Yang-Pi/My-HomeCam-Security/blob/main/report/report.pdf)
