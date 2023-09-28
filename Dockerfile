FROM python:3.9

ADD src .
ADD requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /src

CMD [ "python", "-m", "cdn_prewarm.consumer", "settings.ini" ]

