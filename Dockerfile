FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos las dependencias directamente en el sistema del contenedor, sin entorno virtual aislado
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install --system -r pyproject.toml

FROM python:3.12-slim-bookworm

WORKDIR /app

# Copiamos las librerías instaladas en la etapa anterior directamente al sistema limpio
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiamos la carpeta de código fuente
COPY src /app/src

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "src.fastapi_practice.main:app", "--host", "0.0.0.0", "--port", "8000"]
