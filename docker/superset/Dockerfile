FROM apache/superset
# Switching to root to install the required packages
USER root
RUN pip install psycopg2
USER superset

RUN superset fab create-admin --username admin --firstname Eko --lastname Indarto --email eko.indarto@dans.knaw.nl --password  && \
    superset db upgrade && \
    #superset load_examples && \
    superset init