from typing import Optional
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

class BusinessInsightPrompt:
    @staticmethod
    def context_builder_prompt(
        business_description: str, raw_data: dict
    ) -> list[BaseMessage]:

        system_message = (
            "You are a data context builder for a WhatsApp customer service SaaS platform. "
            "Convert the JSON analytics data into a short, structured narrative. "
            "Include: category totals, change %, and key themes from sample messages. "
            "Be descriptive only — no recommendations."
        )

        human_message = (
            f"Business: {business_description}\n"
            f"Data: {raw_data}\n\n"
            "Summarize this data as a structured context narrative."
            "Write in Indonesian."
        )

        return [SystemMessage(content=system_message), HumanMessage(content=human_message)]

    @staticmethod
    def insight_generator(
        business_description: str, context: Optional[str] = None
    ) -> list[BaseMessage]:

        system_message = (
            "You are a business analyst for a WhatsApp customer service SaaS platform. "
            "The business below uses this SaaS to automate customer service via AI agent on WhatsApp. "
            "Analyze the customer conversation data and generate ONE balanced insight — covering both strengths and issues. "
            "Base your answer only on the context. Be concise. Output structured fields: insight, reason, impact."
        )

        human_message = (
            f"Business: {business_description}\n\n"
            f"Context:\n{context}\n\n"
            "Generate:\n"
            "1. insight — what is happening (positive and/or negative)\n"
            "2. reason — why it is happening (based on data)\n"
            "3. impact — why it matters to the business"
            "Write in Indonesian."
        )

        return [SystemMessage(content=system_message), HumanMessage(content=human_message)]

    @staticmethod
    def recommendation_generator(
        business_description: str,
        insight: Optional[list[str]] = None,
        reason: Optional[str] = None,
        impact: Optional[list[str]] = None,
    ) -> list[BaseMessage]:

        system_message = (
            "You are a business consultant for a SaaS customer service platform. "
            "The business uses an AI WhatsApp agent to handle customer messages. "
            "Give short, practical recommendations based on the insight. "
            "Include both: things to maintain (positive) and things to improve (negative). "
            "Write in Indonesian."
        )

        human_message = (
            f"Bisnis: {business_description}\n\n"
            f"Insight: {insight}\n"
            f"Alasan: {reason}\n"
            f"Dampak: {impact}\n\n"
            "Berikan 2–3 rekomendasi singkat dan spesifik."
        )
        return [SystemMessage(content=system_message), HumanMessage(content=human_message)]