FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    cron \
    vim \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

COPY start.sh .
RUN chmod +x ./start.sh

ENV PYTHONUNBUFFERED=1
ENV TZ=America/Recife
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --no-cache-dir -r requirements.txt

# RUN patchright install --with-deps

COPY . .
RUN echo "30 12 15 * * root bash -c 'set -a; source /app/.env; /usr/local/bin/python3 -m utils.dataloader >> /var/log/cron.log 2>&1'" > /etc/cron.d/investmentCron \    && chmod 0644 /etc/cron.d/investmentCron \
    && crontab /etc/cron.d/investmentCron


RUN touch /var/log/cron.log
# RUN echo "0 9 * * 1,4 python3 /app/utils/dataloader.py >> /var/log/cron.log 2>&1" > /etc/cron.d/investmentCron

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["./start.sh"]