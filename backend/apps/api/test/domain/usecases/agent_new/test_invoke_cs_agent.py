import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4, UUID
import httpx

from src.core.exceptions.agent_exception import AgentNotFound
from src.domain.usecases.agent_new.invoke_cs_agent import (
    InvokeCSAgent,
    InvokeCSAgentInput,
    InvokeCSAgentOutput
)
from src.domain.usecases.interfaces import IAgentRepository

@pytest.fixture
def mock_agent_repo():
    return AsyncMock(spec=IAgentRepository)

@pytest.fixture
def usecase(mock_agent_repo):
    return InvokeCSAgent(agent_repo=mock_agent_repo)

@pytest.fixture
def valid_input():
    return InvokeCSAgentInput(
        agent_id=UUID("a04b8eb2-3b32-44e2-9a6a-bbca2c23ab58"),
        thread_id=str(uuid4()),
        text_message="Hello, test!"
    )

@pytest.mark.asyncio
async def test_execute_success(usecase, mock_agent_repo, valid_input):
    # Arrange
    mock_agent = MagicMock()
    mock_agent.business_id = UUID("06a8a34c-12f8-42c6-bf09-33f2e3a08171")
    mock_agent_repo.get_agent_by_id.return_value = mock_agent

    expected_result = {"status": "success", "response": "Hello back!"}

    with patch("src.domain.usecases.agent_new.invoke_cs_agent.langgraph_client") as mock_langgraph:
        mock_langgraph.run_customer_service_agent = AsyncMock(return_value=expected_result)

        # Act
        result = await usecase.execute(valid_input)

        # Assert
        assert result.is_success is True
        assert result.value == expected_result
        mock_agent_repo.get_agent_by_id.assert_called_once_with(valid_input.agent_id)
        mock_langgraph.run_customer_service_agent.assert_called_once()
        mock_langgraph.register_thread_id.assert_not_called()

@pytest.mark.asyncio
async def test_execute_agent_not_found(usecase, mock_agent_repo, valid_input):
    # Arrange
    mock_agent_repo.get_agent_by_id.return_value = None

    # Act
    result = await usecase.execute(valid_input)

    # Assert
    assert result.is_success is False
    assert result.error == "Agent not found"
    assert isinstance(result.exception, AgentNotFound)
    mock_agent_repo.get_agent_by_id.assert_called_once_with(valid_input.agent_id)

@pytest.mark.asyncio
async def test_execute_langgraph_http_error_retry_success(usecase, mock_agent_repo, valid_input):
    # Arrange
    mock_agent = MagicMock()
    mock_agent.business_id = UUID("06a8a34c-12f8-42c6-bf09-33f2e3a08171")
    mock_agent_repo.get_agent_by_id.return_value = mock_agent

    expected_result = {"status": "retry_success"}
    
    # Create a mock HTTPStatusError
    mock_request = httpx.Request("POST", "http://test")
    mock_response = httpx.Response(404, request=mock_request)
    http_error = httpx.HTTPStatusError("Not Found", request=mock_request, response=mock_response)

    with patch("src.domain.usecases.agent_new.invoke_cs_agent.langgraph_client") as mock_langgraph:
        # First call raises HTTPStatusError, second call succeeds
        mock_langgraph.run_customer_service_agent = AsyncMock(side_effect=[http_error, expected_result])
        mock_langgraph.register_thread_id = AsyncMock()

        # Act
        result = await usecase.execute(valid_input)

        # Assert
        assert result.is_success is True
        assert result.value == expected_result
        mock_agent_repo.get_agent_by_id.assert_called_once_with(valid_input.agent_id)
        assert mock_langgraph.run_customer_service_agent.call_count == 2
        mock_langgraph.register_thread_id.assert_called_once()

@pytest.mark.asyncio
async def test_execute_unexpected_error(usecase, mock_agent_repo, valid_input):
    # Arrange
    mock_agent_repo.get_agent_by_id.side_effect = Exception("Database connection error")

    # Act
    result = await usecase.execute(valid_input)

    # Assert
    assert result.is_success is False
    assert "Unexpected error while invoke customer service agent usecase" in result.error
    assert isinstance(result.exception, Exception)
    assert str(result.exception) == "Database connection error"
