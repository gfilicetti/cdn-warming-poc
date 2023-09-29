FROM python:3.9

COPY requirements.txt /
COPY src/ /src/

RUN pip install -r requirements.txt

WORKDIR /src

CMD [ "python", "-u", "-m", "cdn_prewarm.consumer", "settings.ini" ]

