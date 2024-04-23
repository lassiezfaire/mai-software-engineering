FROM python:3.11-bookworm

WORKDIR /showcase

COPY showcase/requirements.txt ./requirements.txt

RUN python3 -m venv .venv
RUN . .venv/bin/activate

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip install --no-cache-dir 'uvicorn[standard]'

EXPOSE 8000

COPY showcase . 

ENV PYTHONPATH "${PYTHONPATH}:/showcase/product"
ENV PYTHONPATH "${PYTHONPATH}:/showcase/products"

ENTRYPOINT uvicorn main:app --reload --host 0.0.0.0
