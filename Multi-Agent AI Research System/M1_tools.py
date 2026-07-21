from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
import requests 
import os
from rich import print
from dotenv import load_dotenv
load_dotenv(
    
)
tavily = TavilyClient(api_key= os.getenv('TAVILY_API_KEY'))
@tool
def search_tool( topic : str ) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    result = tavily.search(query=topic, max_results=5)
    data = []
    for d in result['results']:
        data.append(
            f""" TITLE: {d['title']} \n
            URL: {d['url']} \n
            CONTENT: {d['content'][:300]} \n"""
        )
    
    return "\n**********\n".join(data)


@tool
def scrape_tool(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    