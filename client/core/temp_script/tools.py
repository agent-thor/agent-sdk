from telethon import TelegramClient, sync
import asyncio
import re

def extract_username(text: str) -> str:
    try:
        # Pattern looks for "username: $" followed by any characters until "$"
        pattern = r'username: \$(.*?)\$'
        
        # Search for the pattern in text
        match = re.search(pattern, text)
        
        if match:
            # Return the captured group (content between $ signs)
            return match.group(1)
        else:
            return None
            
    except Exception as e:
        print(f"Error in regex extraction: {str(e)}")
        return None

async def send_telegram_message(message: str, telegram_cred, username): 
    
    try:
        # Initialize the client
        client = TelegramClient('session_name', telegram_cred['telegram_api_id'], telegram_cred['telegram_api_hash'])
        await client.start()
        # username = extract_username(message)
        
        # Send message to yourself
        await client.send_message(username, message)
        print(f"Message sent successfully: {message}")
        
        # Disconnect the client
        await client.disconnect()
        
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        

# # Example usage
# async def main():
#     await send_telegram_message("Hello! This is a test message.")

# if __name__ == '__main__':
#     asyncio.run(main())


# from telethon import TelegramClient, sync
# import asyncio

# async def initialize_telegram(telegram_cred):
#     try:
#         # Initialize and start the client
#         client = TelegramClient('session_name', telegram_cred['api_id'], telegram_cred['api_hash'])
#         await client.start()
#         return client
#     except Exception as e:
#         print(f"Error initializing Telegram client: {str(e)}")
#         return None

# async def send_telegram_message(client, username, message: str):    
#     try:
#         # Send message to user
#         await client.send_message(username, message)
#         print(f"Message sent successfully: {message}")
#     except Exception as e:
#         print(f"Error sending message: {str(e)}")

# async def cleanup_client(client):
#     try:
#         await client.disconnect()
#     except Exception as e:
#         print(f"Error disconnecting client: {str(e)}")

# async def main():
#     telegram_cred = {
#         'api_id': 'YOUR_API_ID',
#         'api_hash': 'YOUR_API_HASH'
#     }
#     username = 'YOUR_USERNAME'
    
#     # Initialize client
#     client = await initialize_telegram(telegram_cred)
#     if client:
#         # Send message
#         await send_telegram_message(client, username, "Hello! This is a test message.")
#         # Cleanup
#         await cleanup_client(client)

# if __name__ == '__main__':
#     asyncio.run(main())









import tweepy
import time
import os
from datetime import datetime

class TwitterBot:
    """
    A simple Twitter bot that can send tweets using the Tweepy library
    """
    
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Initialize the Twitter bot with API credentials
        
        Args:
            consumer_key (str): Twitter API consumer key
            consumer_secret (str): Twitter API consumer secret
            access_token (str): Twitter API access token
            access_token_secret (str): Twitter API access token secret
        """
        # Authenticate to Twitter
        auth = tweepy.OAuth1UserHandler(
            consumer_key, 
            consumer_secret,
            access_token,
            access_token_secret
        )
        
        # Create API object
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Verify authentication
        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except Exception as e:
            print(f"Error during authentication: {e}")
            raise e
    
    def send_tweet(self, text):
        """
        Send a tweet with the given text
        
        Args:
            text (str): The text content of the tweet (max 280 characters)
            
        Returns:
            tweepy.models.Status: The posted status object
        """
        try:
            if len(text) > 280:
                print(f"Tweet is too long ({len(text)} characters). Truncating to 280 characters.")
                text = text[:277] + "..."
                
            tweet = self.api.update_status(text)
            print(f"Tweet sent successfully! Tweet ID: {tweet.id}")
            return tweet
        except Exception as e:
            print(f"Error sending tweet: {e}")
            return None
    
    def send_tweet_with_media(self, text, media_path):
        """
        Send a tweet with text and media attachment
        
        Args:
            text (str): The text content of the tweet
            media_path (str): Path to the media file to attach
            
        Returns:
            tweepy.models.Status: The posted status object
        """
        try:
            # Upload media
            media = self.api.media_upload(media_path)
            
            # Post tweet with media
            tweet = self.api.update_status(
                status=text,
                media_ids=[media.media_id]
            )
            
            print(f"Tweet with media sent successfully! Tweet ID: {tweet.id}")
            return tweet
        except Exception as e:
            print(f"Error sending tweet with media: {e}")
            return None

    def send_scheduled_tweet(self, text, schedule_time):
        """
        Schedule a tweet to be sent at a specific time
        
        Args:
            text (str): The text content of the tweet
            schedule_time (datetime): When to send the tweet
            
        Returns:
            bool: Whether the tweet was scheduled successfully
        """
        now = datetime.now()
        if schedule_time <= now:
            print("Schedule time must be in the future.")
            return False
            
        # Calculate sleep time in seconds
        sleep_seconds = (schedule_time - now).total_seconds()
        
        print(f"Tweet scheduled for {schedule_time} (in {sleep_seconds:.1f} seconds)")
        
        # Sleep until scheduled time
        time.sleep(sleep_seconds)
        
        # Send the tweet
        return self.send_tweet(text)


# Example usage
if __name__ == "__main__":
    # Twitter API credentials
    # AAAAAAAAAAAAAAAAAAAAAIu4zgEAAAAAK%2FNElVBrHzGiIxYUL7diHHt4cFs%3DdUoi12wOim0pQxsXq4jlFJFIME2UH6U16t4dWi5phWzakS6saV
    consumer_key = "dYgOAzAb7CpMNHzmQMnu4fNGu"
    consumer_secret = "K8N3yy5GoBQBr7818XkpUHuDyltXKDMruwsuqjMOON0045M5uu"
    access_token = "1393640838169710592-MEwjdEI2niYbkcpcENT1QgYhYeluYx"
    access_token_secret = "101oRsPjTn2iiVeX7WJLoZIF81tKU8uGBrLf9hmBbf2Pw"
    
    # Initialize the Twitter bot
    twitter_bot = TwitterBot(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    # Example 1: Send a simple tweet
    twitter_bot.send_tweet("Hello, Twitter! This tweet was sent using the Tweepy library in Python.")
    
    # Example 2: Send a tweet with media
    # twitter_bot.send_tweet_with_media(
    #     "Check out this image!",
    #     "path/to/your/image.jpg"
    # )
    
    # Example 3: Schedule a tweet for 10 seconds in the future
    # from datetime import datetime, timedelta
    # schedule_time = datetime.now() + timedelta(seconds=10)
    # twitter_bot.send_scheduled_tweet(
    #     "This is a scheduled tweet!",
    #     schedule_time
    # )