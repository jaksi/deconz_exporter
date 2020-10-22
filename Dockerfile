FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install .
VOLUME ["/api_keys"]
EXPOSE 9759/tcp
CMD ["deconz_exporter", "--api_key_directory", "/api_keys"]
