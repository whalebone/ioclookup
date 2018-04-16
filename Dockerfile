FROM ubuntu:latest
RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential
COPY ioclookup.py .
RUN pip3 install requests
RUN pip3 install Flask
ENTRYPOINT ["python3"]
CMD ["ioclookup.py"]
