import asyncio
from src.config.supabase import init_supabase, get_supabase
from src.core.agent_configuration_manager import AgentConfigurationManager
from src.business_insight_agent.workflow import BusinessInsightWorkflow
from src.business_insight_agent.nodes import BusinessInsightNodes

def initialize_graph():
    """
    Initialize all dependencies and build the graph.
    LangGraph local server imports this module synchronously.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    # Initialize Supabase client synchronously if not in an event loop
    if loop and loop.is_running():
        raise RuntimeError("Cannot initialize async dependencies inside a running event loop.")
    else:
        asyncio.run(init_supabase())
        
    db = get_supabase()
    
    # Inject database to managers
    agent_configuration_manager = AgentConfigurationManager(db)
    
    # Initialize nodes and workflow
    nodes = BusinessInsightNodes(agent_configuration_manager)
    workflow = BusinessInsightWorkflow(nodes)
    
    return workflow.build()

# LangGraph CLI will look for this 'graph' variable
graph = initialize_graph()
