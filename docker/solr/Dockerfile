FROM solr:8.9.0

ARG WEBHOOK_VERSION=2.6.11
ARG TINI_VERSION=v0.18.0
ARG VERSION=5.6
ARG COLLECTION=collection1
ENV SOLR_OPTS="-Dsolr.jetty.request.header.size=102400"\
    COLLECTION_DIR=${SOLR_HOME}/${COLLECTION}\
    SCRIPT_DIR=${SOLR_HOME}/scripts\
    DATAVERSE_URL=http://dataverse:8080\
    SOLR_USER="solr"\
   DATAVERSE_PKG=https://github.com/IQSS/dataverse/releases/download/v${VERSION}/dvinstall.zip
ENV SCHEMA_SCRIPT_DIR=${SCRIPT_DIR}\
    TARGET=${COLLECTION_DIR}/conf

# Create schema store and scripts folder if not present, change permissions
#USER root
RUN mkdir -p ${SCRIPT_DIR} ${SCHEMA_SCRIPT_DIR} && \
    chown -R ${SOLR_USER}: ${SCRIPT_DIR} ${SCHEMA_SCRIPT_DIR}

# Install tini as minimized init system
RUN wget --no-verbose -O ${SOLR_HOME}/tini https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini && \
    chmod +x ${SOLR_HOME}/tini

# Dataverse uses a **hardcoded** core name "collection1", so we need to use it.
# 1) Create core directory
# 2) Copy _default configset
# 3) Create core.properties
RUN mkdir -p ${COLLECTION_DIR} && \
    cp -a ${PWD}/server/solr/configsets/_default/conf ${COLLECTION_DIR} && \
    echo "name=${COLLECTION}" > ${COLLECTION_DIR}/core.properties
# Download dvinstall.zip, extract, copy schema and config, remove install files
# Copy script for schema creation.
RUN wget --no-verbose -O ${SOLR_HOME}/dvinstall.zip ${DATAVERSE_PKG} && \
    unzip -qq  ${SOLR_HOME}/dvinstall.zip -d ${SOLR_HOME} && \
    mv ${SOLR_HOME}/dvinstall/solrconfig.xml ${COLLECTION_DIR}/conf/solrconfig.xml && \
    mv ${SOLR_HOME}/dvinstall/schema*.xml ${COLLECTION_DIR}/conf/ && \
    mv ${SOLR_HOME}/dvinstall/updateSchemaMDB.sh ${SCHEMA_SCRIPT_DIR}/ && \
    rm -rf ${SOLR_HOME}/dvinstall.zip

# Edit schema.xml to include /schema located files, but fallback to default
#RUN ln -s /schema ${COLLECTION_DIR}/conf/schema && \
#    sed -i -e "s#^.*:include href=\"schema_dv_mdb_fields.*\$#    <xi:include href=\"schema/schema_dv_mdb_fields.xml\" xmlns:xi=\"http://www.w3.org/2001/XInclude\">\n      <xi:fallback><xi:include href=\"schema_dv_mdb_fields.xml\"/></xi:fallback>\n    </xi:include>#" ${COLLECTION_DIR}/conf/schema.xml && \
#    sed -i -e "s#^.*:include href=\"schema_dv_mdb_copies.*\$#    <xi:include href=\"schema/schema_dv_mdb_copies.xml\" xmlns:xi=\"http://www.w3.org/2001/XInclude\">\n      <xi:fallback><xi:include href=\"schema_dv_mdb_copies.xml\"/></xi:fallback>\n    </xi:include>#" ${COLLECTION_DIR}/conf/schema.xml

### SIDECAR BELONGINGS

# Prepare everything for schema update sidecar
RUN wget --no-verbose -O ${SOLR_HOME}/webhook.tar.gz https://github.com/adnanh/webhook/releases/download/${WEBHOOK_VERSION}/webhook-linux-amd64.tar.gz && \
    tar -xzf ${SOLR_HOME}/webhook.tar.gz --strip-components=1 -C ${SCHEMA_SCRIPT_DIR} && \
    chmod +x ${SCHEMA_SCRIPT_DIR}/webhook && \
    rm ${SOLR_HOME}/webhook.tar.gz
COPY --chown=solr:solr schema ${SCHEMA_SCRIPT_DIR}
RUN chmod +x ${SCHEMA_SCRIPT_DIR}/*.sh