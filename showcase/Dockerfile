FROM python:3.11-bookworm

WORKDIR /shop

COPY shop/requirements.txt ./requirements.txt

RUN python3 -m venv .venv
RUN . .venv/bin/activate

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip install --no-cache-dir 'uvicorn[standard]'

EXPOSE 8000

COPY shop . 

ENV PYTHONPATH "${PYTHONPATH}:/shop/databases"
ENV PYTHONPATH "${PYTHONPATH}:/shop/product"
ENV PYTHONPATH "${PYTHONPATH}:/shop/products"
ENV PYTHONPATH "${PYTHONPATH}:/shop/seeder"
ENV PYTHONPATH "${PYTHONPATH}:/shop/shopping_cart"

ENTRYPOINT uvicorn main:app --reload --host 0.0.0.0
