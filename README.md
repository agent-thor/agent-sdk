# Agent SDK

A Python SDK for building and interacting with AI agents.

## Description

Agent SDK is a client library that simplifies the process of creating, configuring, and communicating with AI agents. It provides a clean and intuitive interface for developers to build agent-based applications with minimal setup.

## Features

- Easy agent initialization and configuration
- Support for multiple AI models (OpenAI, etc.)
- Built-in tools for web search, cryptocurrency data, and more
- Telegram integration for messaging
- Conversation management
- Multi-agent system support

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- API keys for various services (OpenAI, Tavily, CoinMarketCap, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agent-sdk.git
cd agent-sdk
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
ELIZA_API_KEY=your_eliza_api_key
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
# Add other necessary API keys
```

## Project Structure

```
agent-sdk/
├── client/
│   ├── core/
│   │   ├── agent.py
│   │   ├── core.py
│   │   ├── conversation.py
│   │   ├── info.py
│   │   └── tools.py
│   ├── models/
│   │   └── agent_model.py
│   ├── utils/
│   ├── data/
│   ├── main.py
│   ├── demo.py
│   └── __init__.py
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Quick Start

Here's a simple example to get started with the Agent SDK:

```python
from client.core.agent import Agent
from client.core.core import InitializeAgent
from client.models.agent_model import Model
from client.core.conversation import IntitializeConversation
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create an AI model
ai_model = Model(
    model="openai", 
    OPENAI_API_KEY=os.getenv('OPENAI_API_KEY'),
    bio=["You interpret web search results", ""],
    lore=["", ""]
)

# Create a web search agent
web_search_agent = Agent(
    name="websearch", 
    agent_name='plugin-web-search',
    TAVILY_API_KEY=os.getenv('TAVILY_API_KEY'),
    model=ai_model
)

# Initialize a multi-agent system
multi_agent = InitializeAgent(
    agents=[web_search_agent], 
    API_KEY=os.getenv('ELIZA_API_KEY'), 
    multi_agent_name="web_search_agent"
)
agent_name = multi_agent.start()

# Start a conversation with the agent
conversation = IntitializeConversation("web_search_agent")
result = conversation.send_query("What is the current weather in New York?")
print(result)
```

## Advanced Usage

Check out the `demo.py` file for more advanced usage examples, including:
- Creating multiple agents with different capabilities
- Setting up a multi-agent system
- Integrating with Telegram for messaging
- Working with cryptocurrency data

## Configuration

The SDK can be configured using environment variables in the `.env` file or by directly passing API keys to the agent constructors.

## Development

To run the tests:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 