FROM python:3.5-alpine

RUN apk update 
RUN apk upgrade 

RUN pip3 install requests 
RUN pip3 install Flask

COPY ioclookup.py .
ENTRYPOINT ["python3"]
CMD ["ioclookup.py"]
