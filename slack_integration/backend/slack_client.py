import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackClient:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def get_recent_messages(self, channel_id, limit=10):
        try:
            result = self.client.conversations_history(
                channel=channel_id,
                limit=limit
            )
            return result["messages"]
        except SlackApiError as e:
            print(f"Error fetching messages: {e}")
            return None

# Example usage (for testing purposes)
if __name__ == "__main__":
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_token:
        print("Error: SLACK_BOT_TOKEN environment variable not set.")
    else:
        client = SlackClient(slack_token)
        # Replace with a real channel ID for testing
        channel_id = "C1234567890"
        messages = client.get_recent_messages(channel_id)
        if messages:
            for message in messages:
                print(message)
