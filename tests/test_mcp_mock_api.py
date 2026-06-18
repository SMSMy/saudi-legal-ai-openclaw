"""
MCP Mock API Tests — Saudi Legal AI Framework
=================================================
Tests tools logic by mocking the Anthropic API client.
Ensures tools handle various model outputs (JSON, markdown, text, errors)
without making real network requests or requiring an API key.
"""
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import httpx
import pytest
from anthropic import APIConnectionError

REPO_ROOT = Path(__file__).parent.parent
MCP_SERVER_PATH = REPO_ROOT / "mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

from tools.analyzer import analyze_clause
from tools.summarizer import summarize_regulation

@pytest.fixture(autouse=True)
def mock_env():
    """Ensure API key is set for tests, so we bypass the missing key check."""
    os.environ["ANTHROPIC_API_KEY"] = "mock-key-for-testing-only"
    yield
    os.environ.pop("ANTHROPIC_API_KEY", None)


def create_mock_message(content_text: str):
    mock_msg = MagicMock()
    mock_content = MagicMock()
    mock_content.text = content_text
    mock_msg.content = [mock_content]
    return mock_msg

# --- analyze_clause tests ---
@patch("tools.analyzer.anthropic.Anthropic")
def test_analyze_valid_json(mock_anthropic):
    mock_client = mock_anthropic.return_value
    expected_json = '{"risk_level": "low"}'
    mock_client.messages.create.return_value = create_mock_message(expected_json)
    
    res = analyze_clause("Test clause", "NDA")
    parsed = json.loads(res)
    assert parsed["risk_level"] == "low"

@patch("tools.analyzer.anthropic.Anthropic")
def test_analyze_markdown_fences(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.return_value = create_mock_message('```json\n{"risk": "high"}\n```')
    
    res = analyze_clause("Test", "NDA")
    parsed = json.loads(res)
    assert parsed["risk"] == "high"

@patch("tools.analyzer.anthropic.Anthropic")
def test_analyze_surrounded_by_text(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.return_value = create_mock_message('Here is the data:\n{"risk": "medium"}\nHope it helps!')
    
    res = analyze_clause("Test", "NDA")
    parsed = json.loads(res)
    assert parsed["risk"] == "medium"

@patch("tools.analyzer.anthropic.Anthropic")
def test_analyze_invalid_json(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.return_value = create_mock_message('Just some text')
    
    res = analyze_clause("Test", "NDA")
    parsed = json.loads(res)
    assert "error" in parsed
    assert "non-JSON" in parsed["error"]
    assert parsed["raw"] == "Just some text"

@patch("tools.analyzer.anthropic.Anthropic")
def test_analyze_api_error(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    mock_client.messages.create.side_effect = APIConnectionError(request=mock_request)
    
    res = analyze_clause("Test", "NDA")
    parsed = json.loads(res)
    assert "error" in parsed
    assert "API error" in parsed["error"]
    assert "mock-key" not in parsed["error"] # API key shouldn't be exposed

def test_analyze_missing_api_key():
    os.environ.pop("ANTHROPIC_API_KEY", None)
    res = analyze_clause("Test", "NDA")
    parsed = json.loads(res)
    assert "error" in parsed
    assert "ANTHROPIC_API_KEY" in parsed["error"]

# --- summarize_regulation tests ---
@patch("tools.summarizer.anthropic.Anthropic")
def test_summarize_valid_json(mock_anthropic):
    mock_client = mock_anthropic.return_value
    expected_json = '{"regulation_name": "Test Law"}'
    mock_client.messages.create.return_value = create_mock_message(expected_json)
    
    res = summarize_regulation("labor-law")
    parsed = json.loads(res)
    assert parsed["regulation_name"] == "Test Law"

@patch("tools.summarizer.anthropic.Anthropic")
def test_summarize_markdown_fences(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.return_value = create_mock_message('```json\n{"regulation_name": "Law"}\n```')
    
    res = summarize_regulation("labor-law")
    parsed = json.loads(res)
    assert parsed["regulation_name"] == "Law"

@patch("tools.summarizer.anthropic.Anthropic")
def test_summarize_surrounded_by_text(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.return_value = create_mock_message('Sure!\n{"regulation_name": "Law"}\nEnjoy.')
    
    res = summarize_regulation("labor-law")
    parsed = json.loads(res)
    assert parsed["regulation_name"] == "Law"

@patch("tools.summarizer.anthropic.Anthropic")
def test_summarize_invalid_json(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.return_value = create_mock_message('Plain text')
    
    res = summarize_regulation("labor-law")
    parsed = json.loads(res)
    assert "error" in parsed
    assert "non-JSON" in parsed["error"]

@patch("tools.summarizer.anthropic.Anthropic")
def test_summarize_api_error(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    mock_client.messages.create.side_effect = APIConnectionError(request=mock_request)
    
    res = summarize_regulation("labor-law")
    parsed = json.loads(res)
    assert "error" in parsed
    assert "API error" in parsed["error"]
    assert "mock-key" not in parsed["error"]

def test_summarize_missing_api_key():
    os.environ.pop("ANTHROPIC_API_KEY", None)
    res = summarize_regulation("labor-law")
    parsed = json.loads(res)
    assert "error" in parsed
    assert "ANTHROPIC_API_KEY" in parsed["error"]
