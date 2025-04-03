#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from core.agent import Agent
from core.core import InitializeAgent
from core.info import AgentInfo
from models.agent_model import Model
from core.conversation import IntitializeConversation
from core.tools import send_telegram_message
import time 
import json


def create_agents():
    # Load keys from json file
    with open('keys.json') as f:
        keys = json.load(f)
    
    ai_model = Model(model="openai", 
                    OPENAI_API_KEY=keys['openai']['api_key'],
                    bio=["You are a trading agent and have a very good knwoledge of trading.", ""],
                    lore=["", ""]
                    )
    
    web_search_agent = Agent(name="websearch", 
                           agent_name='plugin-web-search',
                           TAVILY_API_KEY=keys['tavily']['api_key'],
                           model=ai_model
                           )
    
    coin_agent = Agent(name="market-ethusiastic", 
                      agent_name='plugin-coinmarketcap',
                      COINMARKETCAP_API_KEY=keys['coinmarketcap']['api_key'],
                      model=ai_model
                      )
    
    binance_agent = Agent(name="binance-agent", 
                         agent_name='plugin-binance',
                         BINANCE_API_KEY=keys['binance']['api_key'],
                         BINANCE_SECRET_KEY=keys['binance']['secret_key'],
                         model=ai_model)
    
    telegram_agent = Agent(name="telegram",
                         api_id=keys['telegram']['api_id'],
                         api_hash=keys['telegram']['api_hash'],
                         username=keys['telegram']['username'],
                         phone_no=keys['telegram']['phone_no']
                         )
    
    return ai_model, web_search_agent, coin_agent, binance_agent, telegram_agent


def intialize_agent(ai_model, web_search_agent, coin_agent, binance_agent, telegram_agent):      
    with open('keys.json') as f:
        keys = json.load(f)
        
    multi_agent = InitializeAgent(agents=[web_search_agent, coin_agent, binance_agent], 
                                API_KEY=keys['eliza']['api_key'],
                                multi_agent_name="demo13")
    agent_name = multi_agent.start()
    conversation = IntitializeConversation(agent_name)
    
    return conversation


def create_multi_agent_system(conversation):
    try:
        price_response = conversation.send_query("What is the price of BTC in USD")
        
        if "content" in price_response and "price" in price_response["content"]:
            price = price_response["content"]["price"]
            print(f"Current BTC price: {price}")

            if price > 98000:
                tel_message = f"Price of BTC has reached {price}!"
                telegram_cred = {
                    "telegram_api_id": 23724256,
                    "telegram_api_hash": "e9e6694fcaa2b502c2d2bbae922e4414"
                }
                send_telegram_message(tel_message, telegram_cred, "JoiN9911")

            web_search_response = conversation.send_query("What do you think about BTC prediction this week")
            analysis_query = (
                f"BTC has reached {price} and market research says {web_search_response.get('text', 'no data')}. "
                "What do you think about this? Answer in JSON format with yes or no."
            )
            openai_analysis = conversation.send_query(analysis_query)

            # balance_response = conversation.send_query("Show me my spot Binance balance")
            # print(f"Balance response: {balance_response}")
            trade_response = conversation.send_query("buy me a 2 dot at market price with quantity = 5 ")
        else:
            print("Error: Invalid price response format")
    except Exception as e:
        print(f"Error in multi-agent system: {e}")
            
            
if __name__ == "__main__":
    ai_model, web_search_agent, coin_agent, binance_agent, telegram_agent = create_agents()
    conversation = intialize_agent(ai_model, web_search_agent, coin_agent, binance_agent, telegram_agent)
    
    while True:
        create_multi_agent_system(conversation)
        time.sleep(9)
    
    
   
        
                
    

 






