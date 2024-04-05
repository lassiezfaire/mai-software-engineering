FROM python:3.11-bookworm

WORKDIR /user

COPY user/requirements.txt ./requirements.txt

RUN python3 -m venv .venv
RUN . .venv/bin/activate

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip install --no-cache-dir 'uvicorn[standard]'
RUN pip install --no-cache-dir psycopg2-binary

EXPOSE 8000

COPY user . 

ENV PYTHONPATH "${PYTHONPATH}:/user/user"
ENV PYTHONPATH "${PYTHONPATH}:/user/seeder"

ENTRYPOINT uvicorn main:app --reload --host 0.0.0.0
