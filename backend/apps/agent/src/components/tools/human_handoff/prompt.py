from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage


class HumanHandoffPrompt:
    @staticmethod
    def advocate_agent(
        handoff_reason: str,
        decision_summary: str,
        conversation_summary: str,
    ) -> list[BaseMessage]:
        system_message = """
    You are an Advocate Agent.

    Your role is to create a concise and logical argument supporting why a human handoff should be performed.

    Base your reasoning only on the provided context. Do not invent facts or assumptions.

    Return only one short argument (1-3 sentences).
    """

        human_message = f"""
    Conversation Summary:
    {conversation_summary}

    Decision Summary:
    {decision_summary}

    Handoff Reason:
    {handoff_reason}
    """
        return [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
        ]
    
    @staticmethod
    def critic_agent(
        handoff_reason: str,
        decision_summary: str,
        conversation_summary: str,
    ) -> list[BaseMessage]:
        system_message = """
    You are a Critic Agent.

    Your role is to create a concise and logical argument against performing a human handoff.

    Focus on the strongest reason why the AI should continue handling the conversation instead of escalating it.

    Base your reasoning only on the provided context. Do not invent facts or assumptions.

    Return only one short argument (1-3 sentences).
    """

        human_message = f"""
    Conversation Summary:
    {conversation_summary}

    Decision Summary:
    {decision_summary}

    Handoff Reason:
    {handoff_reason}
    """
        return [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
        ]
    @staticmethod
    def judge_agent(
        handoff_reason: str,
        decision_summary: str,
        conversation_summary: str,
        advocate_argument: str,
        critic_argument: str,
    ) -> list[BaseMessage]:
        system_message = """
    You are a Judge Agent.

    Your role is to objectively evaluate both arguments and decide whether a human handoff should be performed.

    Base your decision only on the provided context and arguments. Do not invent facts or assumptions.

    Return your decision and a brief justification.
    """

        human_message = f"""
    Conversation Summary:
    {conversation_summary}

    Decision Summary:
    {decision_summary}

    Handoff Reason:
    {handoff_reason}

    Advocate Argument:
    {advocate_argument}

    Critic Argument:
    {critic_argument}
    """
        return [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
        ]