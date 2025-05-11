FROM quay.io/jupyter/scipy-notebook:latest
# Chose notebook from https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook

USER root


RUN pip install --no-cache-dir pandas && \
    pip install --pre --no-cache-dir mlflow && \
    pip install --no-cache-dir ray && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# install package XXXX - replace XXXX
# RUN pip install --pre --no-cache-dir XXXX && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"

# based on lab example https://github.com/teaching-on-testbeds/mltrain-chi/blob/main/docker/Dockerfile.jupyter-ray

USER ${NB_UID}
