import os 
import requests

class IntitializeConversation:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        
    def parse_data(self, data_obj):
        """
        Parse data object to extract only text (string) and content (dict) fields.
        
        Args:
            data_obj (dict): Dictionary containing data array
            
        Returns:
            tuple: (text: str, content: dict | None)
        """
        text = ""
        content = None
        
        if not isinstance(data_obj, dict) or 'data' not in data_obj:
            return text, content
            
        for item in data_obj['data']:
            # Extract text if present and is string
            if 'text' in item and isinstance(item['text'], str):
                text = item['text']
                
            # Extract content if present and is dict
            if 'content' in item and isinstance(item['content'], dict):
                content = item['content']
                
        return text, content

    def send_query(self, query, function_name = None):
        """
        Send a query to the Eliza API and return the response.
    
        :param query: The query text to send.
        :return: The API response as a dictionary.
        """
        # Get the full URL from the config file
        url = os.getenv("API_QUERY_ADD")
        
        
        # Prepare the payload
        payload = {
            "query": query,
            "agent_name" : self.agent_name,
            "function_name": function_name
        }
        headers = {"Content-Type": "application/json"}
                
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            
            print(response.json())
            temp = response.json()
            
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            text, content = self.parse_data(response.json())
            response = {
                "text": text,
                "content" : content
                }            
            
            return response
        except requests.exceptions.RequestException as e:
            # Handle request-related errors (e.g., network issues, invalid responses)
            return {"error": "Failed to send query.", "details": str(e)}
        except ValueError as e:
            # Handle JSON decoding errors
            return {"error": "Invalid response from the server.", "details": str(e)}