from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage


class HumanHandoffPrompt:
    @staticmethod
    def advocate_agent(
        handoff_reason: str,
        decision_summary: str,
        conversation_summary: str,
        business_knowladge: dict | None
    ) -> list[BaseMessage]:
        business_knowladge_str = ""
        if business_knowladge:
            for k,v in business_knowladge.items():
                business_knowladge_str += f"* {k}: {v}\n"
        system_message = """
You are an Advocate Agent.

Your role is to create one concise and logical argument supporting why a human handoff should be performed.

Consider the conversation, the AI's decision, the handoff reason, and the available business knowledge.

If the available business knowledge appears sufficient to resolve the customer's issue, acknowledge it instead of forcing a weak argument. Otherwise, explain why a human handoff is still justified.

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

Available Business Knowledge:
{business_knowladge_str if business_knowladge_str else "None"}
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
        business_knowladge: dict | None,
    ) -> list[BaseMessage]:
        business_knowladge_str = ""
        if business_knowladge:
            for k,v in business_knowladge.items():
                business_knowladge_str += f"* {k}: {v}\n"
        system_message = """
You are a Critic Agent.

Your role is to create one concise and logical argument against performing a human handoff.

Carefully review the available business knowledge. If it suggests that the customer's issue may still be resolved using the available knowledge, explain why the AI should continue handling the conversation and indicate which business knowledge should be explored first.

If the available business knowledge is clearly insufficient, acknowledge that instead of forcing a weak argument.

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

Available Business Knowledge:
{business_knowladge_str if business_knowladge_str else "None"}
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
        business_knowladge: dict | None
    ) -> list[BaseMessage]:
        business_knowladge_str = ""
        if business_knowladge:
            for k,v in business_knowladge.items():
                business_knowladge_str += f"* {k}: {v}\n"
        system_message = """
You are a Judge Agent.

Your role is to objectively evaluate both the Advocate and Critic arguments, then decide whether a human handoff is justified.

Before approving a human handoff, determine whether the available business knowledge is sufficient to continue the conversation.

The Main Agent currently has the following tool available:

- get_business_knowledge(): Search and retrieve business knowledge relevant to the customer's issue.

If a human handoff is not justified, recommend how the Main Agent should continue. When appropriate, recommend using get_business_knowledge() and specify the business knowledge topic that should be searched.

Base your decision only on the provided context, arguments, and available business knowledge. Do not invent facts or assumptions.
"""

        human_message = f"""
Conversation Summary:
{conversation_summary}

Decision Summary:
{decision_summary}

Handoff Reason:
{handoff_reason}

Available Business Knowledge:
{business_knowladge_str if business_knowladge_str else "None"}

Advocate Argument:
{advocate_argument}

Critic Argument:
{critic_argument}
"""
        return [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
        ]