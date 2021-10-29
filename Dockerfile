FROM odoo:14


# prepare image for vscode
USER root
RUN mkdir /workspace
RUN apt-get update && apt-get install -y curl git
RUN usermod --shell /bin/bash odoo
RUN pip3 install atlassian-python-api

USER odoo
