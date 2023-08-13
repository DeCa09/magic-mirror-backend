# TODO: see if better base image available
FROM 3.11-slim-bookworm

# Copy function code
COPY model_artifacts model_artifacts/ 

RUN pip3 install pytorch
RUN pip3 install -e .

# don't think reload is for production
CMD [ "uvicorn serving:app --reload" ]