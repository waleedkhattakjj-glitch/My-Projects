from M2_agents import scrape_agent , search_agent , writing_chain , scoring_chain

def research_pipeline(topic : str ) -> str :
    state = {}
    
    # 1) search agent
    print('\n')
    print('................Searching Agent is Working................')
    
    s_agent = search_agent()
    search_result = s_agent.invoke({'messages' : [("user", f"Find recent, reliable and detailed information about: {topic}")]})
    state['state_search_result'] = search_result['messages'][-1].content
    
    # 2) scraping data agent
    print('\n')
    print('................Scraping Agent is Working................')
    
    sc_agent = scrape_agent()
    scrape_result = sc_agent.invoke({'messages' : [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['state_search_result'][:1000]}"
        )]} )
    
    state['state_scrape_result'] = scrape_result['messages'][-1].content
    
    # 3) writing a report
    print('\n')
    print('................Writing Report................')
    
    research = (
        f'SEARCH RESULT : \n {state["state_search_result"]} \n \n',
        f'SCRAPE RESULT : \n {state["state_scrape_result"]}'
    )
    report = writing_chain.invoke({'topic' : topic , 'research' : research})
    state['state_report'] = report
    
    # 4) scoring report
    print('\n')
    print('................Scoring Report................')
    r = state['state_report']
    scoring_report = scoring_chain.invoke({'report' : r })
    state['state_scoring_report'] = scoring_report
    
    
    print('\n \n')
    print('................Final Report................')
    print(state['state_report'])
    
    print('\n \n')
    print('................Final Feedback................')
    print(state['state_scoring_report'])
    
    return state