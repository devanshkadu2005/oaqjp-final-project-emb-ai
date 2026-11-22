"""Emotion detection using the Watson NLP library (final version with error handling)."""
import json

import requests

URL = ("https://sn-watson-emotion.labs.skills.network/v1/"
       "watson.runtime.nlp.v1/NlpService/EmotionPredict")
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return the five emotion scores and the dominant emotion for the given text.

    If the Watson service answers with status code 400 (for example, blank input),
    every value in the returned dictionary is None.
    """
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, json=payload, headers=HEADERS, timeout=10)

    if response.status_code == 400:
        return {**{emotion: None for emotion in EMOTIONS}, "dominant_emotion": None}

    response.raise_for_status()

    formatted_response = json.loads(response.text)
    emotions = formatted_response["emotionPredictions"][0]["emotion"]

    scores = {emotion: emotions[emotion] for emotion in EMOTIONS}
    dominant_emotion = max(scores, key=scores.get)

    return {**scores, "dominant_emotion": dominant_emotion}
