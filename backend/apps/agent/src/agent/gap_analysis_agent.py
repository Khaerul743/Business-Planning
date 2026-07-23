import asyncio
from src.config.supabase import init_supabase, get_supabase
from src.core.agent_configuration_manager import AgentConfigurationManager
from src.gap_analysis_agent.workflow import GapAnalysisWorkflow
from src.gap_analysis_agent.nodes import AgentAnalysisGapNodes

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
    nodes = AgentAnalysisGapNodes(agent_configuration_manager)
    workflow = GapAnalysisWorkflow(nodes)
    
    return workflow.build()

# LangGraph CLI will look for this 'graph' variable
graph = initialize_graph()
