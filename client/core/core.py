import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import json
# from utils.utils import load_json_file
from .utils import load_json_file
import requests
from .character import GenerateCharacter
from dotenv import load_dotenv


load_dotenv()

class InitializeAgent:
    def __init__(self, agents, API_KEY, multi_agent_name):
        """
        Initialize the class with a list of agents.

        :param agents: A list of agent objects or dictionaries.
        :param API_KEY: The API key for authentication.
        """
        self.agents = agents
        self.API_KEY = API_KEY  # Explicitly assign API_KEY
        self.session_id = None  # Initialize session_id as None
        self.agent_id = None
        self.multi_agent_name = multi_agent_name
        

    def display_agents(self):
        """Display details of all agents."""
        for agent in self.agents:
            if isinstance(agent, dict):
                print(f"Agent: {agent.get('name', 'Unknown')}, Attributes: {agent}")
            else:
                print(f"Agent: {agent.name}, Attributes: {agent.__dict__}")

    def generate_character_file(self):
        character_file = load_json_file(os.getenv("CHARACTER_DIR"))
        character = GenerateCharacter(self.agents)
        character_json = character.get_character_info()
        character_json['name'] = self.multi_agent_name
        
        return character_json

    def generate_env_file(self):
        env_file = load_json_file(os.getenv("ENV_DIR"))
        env_json = {}

        for key in env_file.keys():
            for agent in self.agents:
                if hasattr(agent.model, key):
                    env_json[key] = getattr(agent.model, key)
                    
                elif hasattr(agent, key):
                    env_json[key] = getattr(agent, key)

        return env_json
    
    def character_with_env(self, character_file, env_json):
        character_file['settings']['secrets'] = env_json
        
        return character_file
    
    def get_parsed_response(self, response):
        text_output_list = []
        
        for list1 in response:
            text_output_list.append(list1['text'])
        
        return ''.join(text_output_list)
    
    def get_agents_name(self):
        multi_agent_list_name = ''.join([agent.name + '/' for agent in self.agents])
        
        return multi_agent_list_name
    
    def send_query(self, query, agent_id):
        """
        Send a query to the Eliza API and return the response.
    
        :param query: The query text to send.
        :return: The API response as a dictionary.
        """
        # Get the full URL from the config file
        url = os.getenv("API_QUERY_ADD")
        
        
        # Prepare the payload
        payload = {
            "text": query,
            "agent_id" : agent_id
        }
        headers = {"Content-Type": "application/json"}
                
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            output = self.get_parsed_response(response.json())
                        
            return output # Return the JSON response directly
        except requests.exceptions.RequestException as e:
            # Handle request-related errors (e.g., network issues, invalid responses)
            return {"error": "Failed to send query.", "details": str(e)}
        except ValueError as e:
            # Handle JSON decoding errors
            return {"error": "Invalid response from the server.", "details": str(e)}
                

    def start(self):
        """
        Start a new session by hitting the create_session API endpoint.
        Stores the session_id returned by the API.
        env_json and character file is needed for eliza SDK.
        """
        character_file = self.generate_character_file()
        env_json = self.generate_env_file()                 
        character_file = self.character_with_env(character_file, env_json)
        multiple_agents_name = self.get_agents_name()
        

        session_address = os.getenv("API_CREATE_ADD")
        payload = {
            "character_file": character_file,
            "api_key": self.API_KEY,
            "env_json" : env_json,
            "multiple_agents_name" : multiple_agents_name,
            "multi_agent_main_name": self.multi_agent_name
        }
        print(payload)

        headers = {"Content-Type": "application/json"}

        response = requests.post(session_address, data=json.dumps(payload), headers=headers)

        if response.status_code == 201:
            agent_id = response.json()['id']
            print(f"\033[92mAgent_created with id: {agent_id}\033[0m")
            response_data = response.json()
            self.session_id = response_data.get("session_id")  # Store the session_id
            
            return agent_id
        
        elif response.status_code == 403:
            return response.json()

        else:
            print("An error occurred while creating agent.")
            print(response.json())
            
            return None

    def close(self):
        """
        Close the session using the stored session_id.
        """
        if not self.session_id:
            character_file = self.generate_character_file()
            env_file = self.generate_env_file()

            session_address = os.getenv("API_CREATE_ADD")
            payload = {
                "character_file": character_file,
                "env_file": env_file,
                "api_key": self.API_KEY
            }

            headers = {"Content-Type": "application/json"}
            
            session_id_response = requests.post(session_address, data=json.dumps(payload), headers=headers)
            session_id_response_data = session_id_response.json()
            
            if session_id_response.status_code == 500:
                return {"error": "No active session to close."}
            
            else:
                self.session_id = session_id_response_data.get("session_id")

        url = os.getenv("API")
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "api_key": self.API_KEY,
            "session_id": self.session_id  # Include the session_id in the payload
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            self.session_id = None  # Reset the session_id after closing
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}