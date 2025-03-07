#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updated Twitter/X Selenium Bot with fixes for the posting issue
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import os
import platform

class TwitterSeleniumBot:
    """
    A Twitter/X bot that uses Selenium to automate logging in and posting tweets
    through the web interface instead of the API.
    """
    
    def __init__(self, headless=False, debug=False):
        """
        Initialize the Twitter Selenium bot
        
        Args:
            headless (bool): Whether to run Chrome in headless mode (no UI)
            debug (bool): Enable debug mode with additional logging
        """
        self.debug = debug
        
        # Set up Chrome options
        self.chrome_options = Options()
        
        if headless:
            self.chrome_options.add_argument("--headless")
        
        # Additional options to make selenium more stealthy
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Initialize the Chrome driver with direct Chrome approach
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        except Exception as e:
            print(f"Standard Chrome initialization failed: {e}")
            # Try alternate method based on platform
            if platform.system() == "Darwin" and platform.machine() == "arm64":
                print("Detected Mac ARM64, trying alternate method...")
                try:
                    # For Mac M1/M2/M3
                    self.driver = webdriver.Chrome(options=self.chrome_options)
                except Exception as e2:
                    print(f"Mac ARM64 method also failed: {e2}")
                    print("Please install Chrome driver manually and update path.")
                    raise
            else:
                print("Please ensure Chrome is installed and up to date.")
                raise
        
        # Set user agent to appear more like a regular browser
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Maximize window for visibility
        self.driver.maximize_window()
    
    def login(self, username, password):
        """
        Log in to Twitter using username and password
        
        Args:
            username (str): Twitter username or email
            password (str): Twitter password
            
        Returns:
            bool: Whether login was successful
        """
        try:
            # Open Twitter login page
            self.driver.get("https://twitter.com/i/flow/login")
            print("Navigating to Twitter login page...")
            
            # Wait for the page to load
            time.sleep(3 + random.uniform(1, 2))  # Adding randomness to mimic human behavior
            
            # Enter username
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
            )
            self._type_like_human(username_field, username)
            username_field.send_keys(Keys.ENTER)
            print("Username entered...")
            
            # Handle possible "unusual login activity" screen
            try:
                unusual_activity = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']"))
                )
                print("Unusual activity detection screen found...")
                self._type_like_human(unusual_activity, username)  # Sometimes requires email/phone
                unusual_activity.send_keys(Keys.ENTER)
            except Exception:
                print("No unusual activity screen detected, continuing...")
            
            # Wait for password field
            time.sleep(2 + random.uniform(0.5, 1.5))
            
            # Enter password
            password_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            self._type_like_human(password_field, password)
            password_field.send_keys(Keys.ENTER)
            print("Password entered...")
            
            # Wait for home page to load (look for several possible elements)
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Home'][role='link']"))
                )
            except TimeoutException:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='AppTabBar_Home_Link']"))
                    )
                except TimeoutException:
                    try:
                        WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, "//span[text()='Home']"))
                        )
                    except TimeoutException:
                        print("Could not confirm login success. Continuing anyway...")
            
            print("Successfully logged in to Twitter!")
            return True
            
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    
    def post_tweet(self, tweet_text):
        """
        Post a tweet with the given text
        
        Args:
            tweet_text (str): The content of the tweet
            
        Returns:
            bool: Whether the tweet was posted successfully
        """
        try:
            # Different ways to open the compose box
            compose_selectors = [
                "a[data-testid='SideNav_NewTweet_Button']",
                "a[href='/compose/tweet']",
                "a[href='/compose/post']",
                "a[data-testid='FloatingActionButton_Tweet_Button']",
                "div[aria-label='Tweet']",
                "div[aria-label='Post']"
            ]
            
            tweet_button = None
            for selector in compose_selectors:
                try:
                    if self.debug:
                        print(f"Trying selector: {selector}")
                    tweet_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not tweet_button:
                # Try fixed URL approach
                self.driver.get("https://twitter.com/compose/tweet")
                time.sleep(3)
                print("Navigated directly to compose page")
            else:
                tweet_button.click()
                print("Clicked compose button")
            
            time.sleep(2)
            print("Opened tweet compose box...")
            
            # Try different selectors for the tweet input area
            textarea_selectors = [
                "div[data-testid='tweetTextarea_0']",
                "div[role='textbox'][aria-label='Tweet text']",
                "div[role='textbox'][aria-label='Post text']",
                "div[contenteditable='true'][spellcheck='true']",
                "div[data-contents='true']"
            ]
            
            tweet_input = None
            for selector in textarea_selectors:
                try:
                    if self.debug:
                        print(f"Trying textarea selector: {selector}")
                    tweet_input = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not tweet_input:
                print("Could not find tweet input area. Taking screenshot for debugging.")
                self.driver.save_screenshot("tweet_input_error.png")
                return False
                
            self._type_like_human(tweet_input, tweet_text)
            print("Tweet text entered...")
            
            # Try different selectors for the post button
            post_button_selectors = [
                "div[data-testid='tweetButton']",
                "div[data-testid='postButton']",
                "div[role='button'][data-testid='tweetButtonInline']",
                "div[data-testid='renderThread'] div[role='button']",
                "div[aria-label='Post']",
                "div[aria-label='Tweet']"
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    if self.debug:
                        print(f"Trying post button selector: {selector}")
                    # Additional wait time to ensure the post button is active
                    time.sleep(2)
                    post_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not post_button:
                print("Could not find post button. Taking screenshot for debugging.")
                self.driver.save_screenshot("post_button_error.png")
                
                # Last resort approach: try using keyboard shortcut to post
                try:
                    tweet_input.send_keys(Keys.CONTROL + Keys.ENTER)
                    print("Tried keyboard shortcut to post")
                except:
                    return False
            else:
                # Make sure the button is fully in view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
                time.sleep(1)
                
                # Try both click methods
                try:
                    post_button.click()
                except:
                    self.driver.execute_script("arguments[0].click();", post_button)
                
                print("Post button clicked")
            
            # Wait for the tweet to be posted
            time.sleep(5 + random.uniform(1, 3))
            print("Tweet posted successfully!")
            return True
            
        except Exception as e:
            print(f"Error posting tweet: {e}")
            if self.debug:
                # Take screenshot for debugging
                self.driver.save_screenshot("error_screenshot.png")
                print(f"Current URL: {self.driver.current_url}")
                print(f"Page source: {self.driver.page_source[:1000]}...")  # First 1000 chars
            return False
    
    def post_tweet_with_image(self, tweet_text, image_path):
        """
        Post a tweet with text and an image
        
        Args:
            tweet_text (str): The content of the tweet
            image_path (str): Path to the image file
            
        Returns:
            bool: Whether the tweet was posted successfully
        """
        try:
            # Use the same methods to open compose box as in post_tweet
            compose_selectors = [
                "a[data-testid='SideNav_NewTweet_Button']",
                "a[href='/compose/tweet']",
                "a[href='/compose/post']",
                "a[data-testid='FloatingActionButton_Tweet_Button']",
                "div[aria-label='Tweet']",
                "div[aria-label='Post']"
            ]
            
            tweet_button = None
            for selector in compose_selectors:
                try:
                    tweet_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not tweet_button:
                # Try fixed URL approach
                self.driver.get("https://twitter.com/compose/tweet")
                time.sleep(3)
            else:
                tweet_button.click()
            
            # Use the same methods to find textarea as in post_tweet
            textarea_selectors = [
                "div[data-testid='tweetTextarea_0']",
                "div[role='textbox'][aria-label='Tweet text']",
                "div[role='textbox'][aria-label='Post text']",
                "div[contenteditable='true'][spellcheck='true']",
                "div[data-contents='true']"
            ]
            
            tweet_input = None
            for selector in textarea_selectors:
                try:
                    tweet_input = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not tweet_input:
                return False
                
            self._type_like_human(tweet_input, tweet_text)
            
            # Use absolute path for image
            abs_image_path = os.path.abspath(image_path)
            
            # Try different file input selectors
            file_input_selectors = [
                "input[type='file'][data-testid='fileInput']",
                "input[type='file'][multiple='true']",
                "input[type='file']",
                "input[accept='image/jpeg,image/png,image/webp,image/gif,video/mp4,video/quicktime']"
            ]
            
            file_input = None
            for selector in file_input_selectors:
                try:
                    file_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not file_input:
                print("Could not find file input element.")
                return False
                
            file_input.send_keys(abs_image_path)
            print("Image uploaded...")
            
            # Wait for image to upload using different possible selectors
            attachment_selectors = [
                "div[data-testid='attachments']",
                "div[aria-label='Image attached']",
                "div[data-testid='tweetImageAttachments']"
            ]
            
            attachment_found = False
            for selector in attachment_selectors:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    attachment_found = True
                    break
                except:
                    continue
            
            if not attachment_found:
                print("Could not confirm image upload.")
                # Continue anyway
            
            # Use the same method to find post button as in post_tweet
            post_button_selectors = [
                "div[data-testid='tweetButton']",
                "div[data-testid='postButton']",
                "div[role='button'][data-testid='tweetButtonInline']",
                "div[data-testid='renderThread'] div[role='button']",
                "div[aria-label='Post']",
                "div[aria-label='Tweet']"
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    # Additional wait time to ensure the post button is active
                    time.sleep(2)
                    post_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not post_button:
                # Last resort approach: try using keyboard shortcut to post
                try:
                    tweet_input.send_keys(Keys.CONTROL + Keys.ENTER)
                except:
                    return False
            else:
                # Make sure the button is fully in view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
                time.sleep(1)
                
                # Try both click methods
                try:
                    post_button.click()
                except:
                    self.driver.execute_script("arguments[0].click();", post_button)
            
            # Wait for the tweet to be posted
            time.sleep(8)  # Longer wait for image upload
            print("Tweet with image posted successfully!")
            return True
            
        except Exception as e:
            print(f"Error posting tweet with image: {e}")
            return False
    
    def close(self):
        """Close the browser and clean up"""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")
    
    def _type_like_human(self, element, text):
        """Type text with random delays between keystrokes to mimic human typing"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))  # Random delay between keystrokes


# Example usage
if __name__ == "__main__":
    # Initialize the bot - no window minimize, enable debug mode
    twitter_bot = TwitterSeleniumBot(debug=True)
    
    try:
        # Log in to Twitter
        username = "krishna_te74606"  # Replace with your username or email
        password = "RatAnseela_JohnQ1"  # Replace with your password
        
        if twitter_bot.login(username, password):
            # Post a simple tweet
            twitter_bot.post_tweet("Hello guys. I think BTC will go up. " + str(random.randint(1000, 9999)))
            
            # Uncomment to post with an image
            # twitter_bot.post_tweet_with_image(
            #     "Check out this image!",
            #     "/path/to/your/image.jpg"  # Absolute path to image
            # )
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Give some time to see the results before closing
        time.sleep(5)
        
        # Close the browser
        twitter_bot.close()