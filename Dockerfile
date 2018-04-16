FROM ubuntu:latest
RUN apt-get update -y && apt-get install -y python3-pip && \
    pip3 install requests Flask
COPY ioclookup.py .
ENTRYPOINT ["python3"]
CMD ["ioclookup.py"]
