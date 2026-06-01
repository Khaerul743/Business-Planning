from typing import Literal, List, Sequence, Any
from langchain_openai import ChatOpenAI
from shared.utils.logger import get_logger
from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class BaseNode:
    def __init__(self, name):
        self._logger = get_logger(name)
        self._llm = None

    def llm(
        self,
        provider: Literal["openai", "anthropic", "google"],
        model: str,
        temperature: float,
    ):
        if self._llm is None:
            self._llm = self._get_llm_provider(provider, model, temperature)
        self._logger.info(f"Initialized LLM provider: {provider} ({model})")
        return self._llm

    def _get_llm_provider(
        self,
        provider: Literal["openai", "anthropic", "google"],
        model: str,
        temperature: float,
    ):
        match provider:
            case "openai":
                return ChatOpenAI(model=model, temperature=temperature)
            case "anthropic":
                return ChatOpenAI(model=model)
            case "google":
                return ChatOpenAI(model=model)
            case _:
                return ChatOpenAI(model="gpt-4o-mini")

    async def invoke_model(
        self,
        provider: Literal["openai", "anthropic", "google"],
        model: str,
        temperature: float,
        messages: list[Any],
    ):
        try:
            llm_model = self.llm(provider, model, temperature)
            response = await llm_model.ainvoke(messages)
            return response
        except Exception as e:
            self._logger.error(f"Error while invoke llm model: {e}")
            raise e

    def invoke_llm_with_structured_output(
        self,
        provider: Literal["openai", "anthropic", "google"],
        model: str,
        temperature: float,
        messages: list[Any],
        output_model: type[BaseModel],
        output_type: Literal["base", "dict"] = "base",
    ):
        """Call LLM and return a parsed pydantic model instance as a dictionary (structured output)."""
        try:
            llm_model = self.llm(provider, model, temperature).with_structured_output(
                output_model
            )

            if hasattr(llm_model, "ainvoke"):
                response = llm_model.ainvoke(messages)
            else:
                raise TypeError("Provided LLM does not support invoke/ainvoke.")

            if output_type == "base":
                return response

            # If the LLM already returned a dict, return it directly
            if isinstance(response, dict):
                return response

            # If the LLM returned a BaseModel instance, convert to dict (supports pydantic v1 & v2)
            if isinstance(response, BaseModel):
                try:
                    if hasattr(response, "model_dump"):
                        return response.model_dump()  # pydantic v2
                    return response.dict()  # pydantic v1
                except Exception as e:
                    self._logger.error(
                        f"Failed to convert BaseModel response to dict: {e}"
                    )
                    raise

            # Otherwise, attempt to parse the raw response into the provided pydantic model then convert to dict
            try:
                parsed = output_model.parse_obj(response)  # type: ignore[arg-type]
                if hasattr(parsed, "model_dump"):
                    return parsed.model_dump()
                return parsed.dict()
            except Exception as e:
                self._logger.error(
                    f"Failed to parse LLM response into {output_model} and convert to dict: {e}"
                )
                raise

        except Exception as e:
            self._logger.error(f"Error while invoking LLM: {e}")
            raise

    def get_all_previous_messages(
        self, messages: Sequence[BaseMessage], max_trim: int = 0
    ):
        if max_trim != 0:
            all_previous_messages = messages[-max_trim:]
        else:
            all_previous_messages = messages

        return all_previous_messages

    def get_prompt_setup(
        self,
        agent_prompt: List[BaseMessage],
        state_messages: Sequence[BaseMessage],
        max_trim: int = 0,
    ) -> List[Any]:
        all_previous_messages = self.get_all_previous_messages(state_messages, max_trim)
        setup_prompt: list[Any] = (
            [agent_prompt[0]] + list(all_previous_messages) + [agent_prompt[1]]
        )
        return setup_prompt
