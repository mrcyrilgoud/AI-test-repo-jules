class MessageClassifier:
    def __init__(self):
        self.rules = {
            "Urgent": ["urgent", "asap", "important"],
            "Question": ["?", "what", "where", "when", "who", "why", "how"],
            "Task": ["task", "todo", "add to my board", "create a ticket"],
        }

    def classify(self, message_text):
        """
        Classifies a message based on keywords.
        The classification is designed to be pluggable and can be replaced
        by a more sophisticated model later.
        """
        message_lower = message_text.lower()
        for category, keywords in self.rules.items():
            if any(keyword in message_lower for keyword in keywords):
                return category
        return "General"

# Example usage (for testing purposes)
if __name__ == "__main__":
    classifier = MessageClassifier()
    messages_to_test = [
        "This is an urgent request!",
        "Can you help me with this?",
        "Please add this to my board.",
        "Just a general update.",
    ]
    for message in messages_to_test:
        category = classifier.classify(message)
        print(f"Message: '{message}' -> Category: {category}")
