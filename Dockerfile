# Використовуємо офіційний образ Python 3.11
FROM python:3.11

# Встановлюємо pipenv
RUN pip install pipenv

# Копіюємо всі файли з поточного каталогу у контейнер
COPY . /cli_bot

# Встановлюємо залежності за допомогою pipenv
WORKDIR /cli_bot
RUN pipenv --python 3.11 install --deploy

# Запускаємо скрипт після старту контейнера
CMD ["python", "cli_bot_final.py"]
