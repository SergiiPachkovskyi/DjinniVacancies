FROM python:3.10

RUN mkdir -p /DjinniVacancies/
WORKDIR /DjinniVacancies/

COPY . /DjinniVacancies/
ENV TOKEN '5210162656:AAERvYP0NbXi92bW4_-TheeQWya-wsOS88w'
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
