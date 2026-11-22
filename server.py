"""Flask web server for the emotion detection application."""
from flask import Flask, render_template, request
import requests

from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

INVALID_TEXT_MESSAGE = "Invalid text! Please try again!"


@app.route("/emotionDetector")
def emot_detector():
    """Analyze the text passed in the 'textToAnalyze' query parameter.

    Returns a sentence describing the emotion scores and the dominant emotion,
    or an error message when the input is blank or invalid.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")

    try:
        response = emotion_detector(text_to_analyze)
    except requests.RequestException:
        return "The emotion detection service is unavailable. Please try again later."

    if response["dominant_emotion"] is None:
        return INVALID_TEXT_MESSAGE

    return (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


@app.route("/")
def render_index_page():
    """Render the main page of the application."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
