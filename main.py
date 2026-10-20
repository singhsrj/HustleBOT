# To install: pip install tavily-python
from tavily import TavilyClient
client = TavilyClient("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")
response = client.search(
    query="How big is the digital fitness and AI coaching market?"
)
print(response)