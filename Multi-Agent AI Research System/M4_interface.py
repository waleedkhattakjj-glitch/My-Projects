import streamlit as st

# The interface runs each stage itself so its progress and the exact tool outputs
# can be shown separately in the application.
from M2_agents import scrape_agent, search_agent, scoring_chain, writing_chain


st.set_page_config(page_title="Research Studio", page_icon="✦", layout="wide")

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');
      .stApp {
        background:
          radial-gradient(circle at 8% 5%, rgba(130, 87, 229, .18), transparent 25rem),
          radial-gradient(circle at 91% 12%, rgba(7, 183, 175, .15), transparent 27rem),
          #f7f8fc;
        font-family: 'DM Sans', sans-serif;
      }
      .block-container { max-width: 1220px; padding: 2.7rem 2rem 4rem; }
      .brand { text-align: center; padding: .6rem 0 2.2rem; }
      .brand-badge {
        display: inline-block; color: #6443cf; background: #ede9ff; border-radius: 99px;
        padding: .32rem .78rem; font-weight: 700; font-size: .78rem; letter-spacing: .08em;
      }
      .brand h1 { font-family: 'Playfair Display', serif; color: #1d2440; font-size: 3rem; margin: .6rem 0 .3rem; }
      .brand p { color: #65708b; font-size: 1.05rem; margin: 0; }
      div[data-testid="stForm"] {
        background: rgba(255,255,255,.92); border: 1px solid #e6e9f2; border-radius: 19px;
        padding: 1.15rem 1.25rem .35rem; box-shadow: 0 14px 35px rgba(40, 48, 83, .09);
      }
      div[data-testid="stTextInput"] input { border-radius: 10px; border: 1px solid #dce1ee; }
      .stFormSubmitButton > button {
        background: linear-gradient(110deg, #6242ce, #267bd8); border: 0; border-radius: 10px;
        font-weight: 700; height: 2.7rem; width: 100%;
      }
      .stButton > button {
        background: white; color: #303b5c; border: 1px solid #dce2f0; border-radius: 10px;
        font-weight: 650; text-align: left; padding: .65rem .8rem; width: 100%;
      }
      .stButton > button:hover { color: #5d3aca; border-color: #8669e2; background: #f8f6ff; }
      .rail {
        padding: 1.2rem; background: rgba(255,255,255,.76); border: 1px solid #e7eaf3;
        border-radius: 16px; position: sticky; top: 1rem;
      }
      .rail-title { color: #1d2440; font-weight: 700; font-size: 1rem; margin: 0 0 .25rem; }
      .rail-text { color: #75809a; font-size: .83rem; margin: 0 0 1rem; }
      .report-card {
        background: white; border: 1px solid #e5e9f2; box-shadow: 0 12px 32px rgba(36, 45, 75, .06);
        border-radius: 17px; padding: 1.7rem 1.9rem;
      }
      .card-heading { color:#1e2745; font-size: 1.28rem; font-weight: 750; margin-bottom: .9rem; }
      .detail-label { color:#6443cf; font-weight:700; font-size:.88rem; margin: 1rem 0 .5rem; }
      .stStatus { border-radius: 14px; }
    </style>
    <div class="brand">
      <span class="brand-badge">MULTI-AGENT RESEARCH</span>
      <h1>Research Studio</h1>
      <p>From web discovery to a reviewed research report — in one focused workflow.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def tool_content(agent_result, tool_name):
    """Return the real content returned by a LangChain tool call."""
    messages = agent_result.get("messages", [])
    content = [
        str(message.content)
        for message in messages
        if getattr(message, "name", None) == tool_name
    ]
    if content:
        return "\n\n".join(content)
    # Fallback to the agent's final response if no ToolMessage is available.
    return str(messages[-1].content) if messages else "No output was returned."


def run_research(topic):
    """The same four stages as M3_pipeline.py, executed by the UI itself."""
    state = {}

    with st.status("Preparing the research workflow…", expanded=True) as progress:
        # 1. Search
        progress.update(label="1 of 4 · Searching agent is working…", state="running")
        st.write("🔎 **Searching Agent is Working**")
        search_result = search_agent().invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
        )
        state["state_search_result"] = tool_content(search_result, "search_tool")

        # 2. Scrape
        progress.update(label="2 of 4 · Scraping agent is working…", state="running")
        st.write("📄 **Scraping Agent is Working**")
        scrape_result = scrape_agent().invoke(
            {"messages": [("user",
                f"Based on the following search results about '{topic}', "
                "pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['state_search_result'][:1000]}")]} 
        )
        state["state_scrape_result"] = tool_content(scrape_result, "scrape_tool")

        # 3. Write
        progress.update(label="3 of 4 · Writing report…", state="running")
        st.write("✍️ **Writing Report**")
        research = (
            f"SEARCH RESULT:\n{state['state_search_result']}\n\n"
            f"SCRAPE RESULT:\n{state['state_scrape_result']}"
        )
        state["state_report"] = writing_chain.invoke({"topic": topic, "research": research})

        # 4. Score
        progress.update(label="4 of 4 · Scoring report…", state="running")
        st.write("✓ **Scoring Report**")
        state["state_scoring_report"] = scoring_chain.invoke({"report": state["state_report"]})
        progress.update(label="Research workflow completed", state="complete", expanded=False)

    return state


with st.form("topic_form"):
    topic = st.text_input("What would you like to research?", placeholder="e.g. Renewable energy adoption in Pakistan")
    submitted = st.form_submit_button("Generate report  →")

if submitted:
    if not topic.strip():
        st.warning("Enter a topic before generating the report.")
    else:
        try:
            st.session_state.research_state = run_research(topic.strip())
            st.session_state.active_detail = None
            st.session_state.research_topic = topic.strip()
        except Exception as error:
            st.error(f"The research workflow could not be completed: {error}")

if "research_state" in st.session_state:
    state = st.session_state.research_state
    st.markdown("<br>", unsafe_allow_html=True)
    rail, content = st.columns([1, 3.15], gap="large")

    with rail:
        st.markdown('<div class="rail">', unsafe_allow_html=True)
        st.markdown('<p class="rail-title">Agent outputs</p>', unsafe_allow_html=True)
        st.markdown('<p class="rail-text">Inspect the exact data collected by each agent.</p>', unsafe_allow_html=True)
        if st.button("🔎  View searching agent results", key="search_button"):
            st.session_state.active_detail = "search"
        if st.button("📄  View scraping agent results", key="scrape_button"):
            st.session_state.active_detail = "scrape"
        st.markdown("</div>", unsafe_allow_html=True)

    with content:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        if st.session_state.get("active_detail") == "search":
            st.markdown('<div class="card-heading">Searching Agent Results</div>', unsafe_allow_html=True)
            st.markdown('<div class="detail-label">Raw search results returned by search_tool</div>', unsafe_allow_html=True)
            st.code(state.get("state_search_result", "No search results were returned."), language=None)
        elif st.session_state.get("active_detail") == "scrape":
            st.markdown('<div class="card-heading">Scraping Agent Results</div>', unsafe_allow_html=True)
            st.markdown('<div class="detail-label">Clean page text returned by scrape_tool</div>', unsafe_allow_html=True)
            st.text_area("Scraped content", state.get("state_scrape_result", "No scraped content was returned."), height=480, disabled=True, label_visibility="collapsed")
        else:
            st.markdown('<div class="card-heading">Research Report</div>', unsafe_allow_html=True)
            st.markdown(state.get("state_report", "No report was returned."))
            st.divider()
            st.markdown('<div class="card-heading">Report Feedback</div>', unsafe_allow_html=True)
            st.markdown(state.get("state_scoring_report", "No feedback was returned."))
        st.markdown("</div>", unsafe_allow_html=True)
