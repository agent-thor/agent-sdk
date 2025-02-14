import os 
from dotenv import load_dotenv
import requests
from typing import Dict, Any, Optional

load_dotenv()

class AgentInfo:
    def __init__(self, api_key: str):
        """
        Initialize AgentInfo with API key
        
        Args:
            api_key (str): API key for authentication
        """
        self.api_key = api_key
        
    def get_agent_info(self, user_id: str) -> Dict[str, Any]:
        """
        Get agent information by making POST request to API
        
        Args:
            user_id (str): ID of the user to get agent info for
            
        Returns:
            Dict[str, Any]: Response from the API
            
        Raises:
            requests.RequestException: If API request fails
            KeyError: If required environment variable is missing
            Exception: For other unexpected errors
        """
        try:
            url = os.getenv("API_AGENT_INFO_ADD")
            if not url:
                raise KeyError("API_AGENT_INFO_ADD environment variable is not set")
            
            # Prepare request data
            payload = {
                "api_key": self.api_key,
                "user_id": user_id
            }
            
            # Make POST request
            response = requests.post(
                url=url,
                json=payload,
                headers={
                    "Content-Type": "application/json"
                }
            )
            
            # Raise exception for bad status codes
            response.raise_for_status()
            
            # Return JSON response
            return response.json()
            
        except requests.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except KeyError as e:
            raise KeyError(f"Configuration error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")