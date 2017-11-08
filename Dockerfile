FROM sqlguard:latest
LABEL maintainer="will<will835559313@163.com>"

COPY ./src /code
WORKDIR /code/app
EXPOSE 5000 5506
#RUN wget http://repo.percona.com/release/7/RPMS/x86_64/Percona-Server-devel-55-5.5.57-rel38.9.el7.x86_64.rpm && \
#rpm -ivh Percona-Server-devel-55-5.5.57-rel38.9.el7.x86_64.rpm
#RUN wget 'http://repo.percona.com/release/7/RPMS/x86_64/Percona-Server-client-55-5.5.57-rel38.9.el7.x86_64.rpm' && \
#rpm -ivh Percona-Server-client-55-5.5.57-rel38.9.el7.x86_64.rpm
RUN rpm -ivh *.rpm
RUN yum install -y python-pip python-devel && \
pip install -r requirements.txt -i https://pypi.douban.com/simple

CMD gunicorn -w 4 -b 0.0.0.0:5000 app:app --daemon && Inception --port 5506
