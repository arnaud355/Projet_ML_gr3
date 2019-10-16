FROM mongo
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN apt update
RUN apt -y upgrade
RUN apt install -y python3-pip
RUN python3 -m pip install pandas
RUN python3 -m pip install pymongo
#RUN pip install -r requirements.txt
#ENTRYPOINT ["python3"]
#VOLUME . /app
CMD ["/bin/bash"]

#FROM mongo
#WORKDIR /app
