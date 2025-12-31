FROM python:3.11-alpine


RUN echo "Drivault Image is building"
WORKDIR /drivault
RUN echo $(pip --version)
RUN pip3 install poetry

COPY poetry.lock pyproject.toml ./

# Copy the app directory into the working directory
COPY app/ ./app/

RUN poetry install --no-root

# IMPORTANT: No need to activate venv manually, poetry takes care
# Expose the port that uvicorn will run on
EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]