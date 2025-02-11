from core.agent import Agent
from core.core import InitializeAgent
from models.agent_model import Model

print("Import done")

ai_model = Model(model = "openai", 
                  OPENAI_API_KEY= '', 
                  bio = [
                      "You are a market ethusisatic who fetches price",
                      ""
                      ],
                  lore = [
                      "",
                      ""
                      ]
                 
                  )



web_search_agent = Agent(name = "websearch", 
                          agent_name = 'plugin-web-search', 
                          TAVILY_API_KEY='',
                          model = ai_model
                            )

# coin_agent = Agent(name = "market-ethusiastic", 
#                           agent_name = 'plugin-coinmarketcap', 
#                           COINMARKETCAP_API_KEY= '574384e6-e75a-4f14-8483-50527138e394',
#                           model = ai_model
#                             )

# binance_agent = Agent(name = "binance-agent", 
#                           agent_name = 'plugin-binance', 
#                           BINANCE_API_KEY= '',
#                           BINANCE_SECRET_KEY = '',
#                           model = ai_model)


multi_agent = InitializeAgent(agents = [web_search_agent], API_KEY= "", multi_agent_name = "web_search")
multi_agent.start()
# multi_agent.close()

# multi_agent.agent_id

"""
coinmarketcap
"""
# output = multi_agent.send_query("what is your name")
# output = multi_agent.send_query("what is the price of BTC this week")
# output = multi_agent.send_query("and what do you think about coming weeks price? give me analysis based on previous bitcoin price")

# print(output)


"""
binance
"""
