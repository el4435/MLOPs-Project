FROM quay.io/jupyter/scipy-notebook:latest
# Chose notebook from https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook


USER ${NB_UID}

# Install pandas
RUN pip install --no-cache-dir pandas

# Install mlflow
RUN pip install --pre --no-cache-dir mlflow

# Install Ray using conda
RUN pip install --no-cache-dir ray==2.42.1 && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Fix permissions
RUN fix-permissions "${CONDA_DIR}"
RUN fix-permissions "/home/${NB_USER}"

# install package XXXX - replace XXXX
# RUN pip install --pre --no-cache-dir XXXX && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"

# based on lab example https://github.com/teaching-on-testbeds/mltrain-chi/blob/main/docker/Dockerfile.jupyter-ray


