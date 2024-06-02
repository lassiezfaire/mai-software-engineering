FROM python:3.11-bookworm

WORKDIR /api-gateway

COPY api-gateway/requirements.txt ./requirements.txt

RUN python3 -m venv .venv
RUN . .venv/bin/activate

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip install --no-cache-dir 'uvicorn[standard]'

EXPOSE 8000

COPY api-gateway .

ENV PYTHONPATH "${PYTHONPATH}:/api-gateway"

ENTRYPOINT uvicorn main:app --reload --host 0.0.0.0
