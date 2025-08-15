#!/bin/bash
export PYTHONPATH=/app

# Inicia cron no foreground
cron -f &

# Inicia FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info &

# Mantém o container ativo mostrando logs do cron
tail -f /var/log/cron.log