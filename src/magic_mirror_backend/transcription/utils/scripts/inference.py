import os
import logging
import pickle

import torch

logger = logging.getLogger()
logger.setLevel(logging.INFO)



DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_TO_MODEL_ARTIFACTS = os.path.join(DIR_PATH, "..", "model_artifacts/")
MODEL_ARTIFACT_NAME = "transcription_model.pickle"

with open(os.path.join(PATH_TO_MODEL_ARTIFACTS, MODEL_ARTIFACT_NAME), "rb") as inputfile:
    audio_transcription_model = pickle.load(inputfile)

if torch.cuda.is_available():
    audio_transcription_model.cuda()
    print("Don't worry. GPU is used, brother.")
