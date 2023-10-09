FROM geopraevent/python-poetry:1.6.1-python3.10-bullseye

# 
WORKDIR /code

# 
COPY ./pyproject.toml /code/pyproject.toml

RUN poetry install
# 
COPY ./main.py /code/main.py
COPY ./core /code/core

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]