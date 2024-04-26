# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.11

# Встановимо змінну середовища
ENV CLI_HOME /cli_bot

# Встановимо робочу директорію всередині контейнера
WORKDIR $CLI_HOME

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Встановимо залежності всередині контейнера
RUN pip install pipenv
COPY Pipfile Pipfile.lock /cli_bot/
RUN pipenv install --deploy --system

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 5000

# Запускаємо образ всередині контейнера
CMD ["python", "cli_bot_final.py"]