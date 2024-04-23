import os
import pandas as pd
import numpy as np
from setting import config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class C_SLACKALERT:
    def __init__(self, logger):
        self.client = WebClient(token=config.SLACK_BOT_TOKEN)
        self.logger = logger
        
    def send_msg(self, txt_message):
        try:
            # Call the chat.postMessage method using the WebClient
            result = self.client.chat_postMessage(
                channel=config.SLACK_CHANNEL_ID,
                text=txt_message
            )
            self.logger.info(result)
        except SlackApiError as e:
            self.logger.error(f"Error posting message: {e}")