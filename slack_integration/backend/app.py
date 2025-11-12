from flask import Flask, jsonify
from message_classifier import MessageClassifier

app = Flask(__name__)
classifier = MessageClassifier()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/messages")
def get_classified_messages():
    # For now, we'll use mock data to simulate fetching messages from Slack.
    # In a real implementation, this would call the SlackClient.
    mock_messages = [
        {"ts": "1678886400.000100", "user": "U12345", "text": "This is an urgent task that needs to be done ASAP."},
        {"ts": "1678886460.000200", "user": "U67890", "text": "What is the status of the project?"},
        {"ts": "1678886520.000300", "user": "U12345", "text": "Please add the design mockups to the project board."},
        {"ts": "1678886580.000400", "user": "U67890", "text": "Thanks for the update!"},
    ]

    classified_messages = []
    for message in mock_messages:
        category = classifier.classify(message["text"])
        classified_message = {**message, "category": category}
        classified_messages.append(classified_message)

    return jsonify(classified_messages)

if __name__ == "__main__":
    app.run(debug=True)
