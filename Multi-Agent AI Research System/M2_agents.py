from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from M1_tools import search_tool,scrape_tool
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

def search_agent():
    agent = create_agent(
        model= model,
        tools= [search_tool]
    )
    return agent


def scrape_agent():
    agent = create_agent(
        model= model,
        tools= [scrape_tool]
    )
    return agent

writing_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])
parser = StrOutputParser()
writing_chain = writing_prompt | model | parser

scoring_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

scoring_chain = scoring_prompt | model | parser