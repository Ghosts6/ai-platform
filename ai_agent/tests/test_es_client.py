
import pytest
from unittest.mock import patch, MagicMock
from django.conf import settings
from ai_agent.shared_utils.es_client import get_es_client

@pytest.mark.django_db
@patch('ai_agent.shared_utils.es_client.Elasticsearch')
def test_get_es_client_success(mock_elasticsearch):
    """
    Tests that get_es_client returns a client when the connection is successful.
    """
    # Arrange
    mock_client = MagicMock()
    mock_client.ping.return_value = True
    mock_elasticsearch.return_value = mock_client
    settings.ELASTICSEARCH_HOST = 'http://localhost:9200'

    # Act
    client = get_es_client()

    # Assert
    assert client is not None
    assert client == mock_client
    mock_elasticsearch.assert_called_once_with(hosts=['http://localhost:9200'])
    client.ping.assert_called_once()

@pytest.mark.django_db
@patch('ai_agent.shared_utils.es_client.Elasticsearch')
def test_get_es_client_ping_fails(mock_elasticsearch):
    """
    Tests that get_es_client returns None when the ping fails.
    """
    # Arrange
    mock_client = MagicMock()
    mock_client.ping.return_value = False
    mock_elasticsearch.return_value = mock_client
    settings.ELASTICSEARCH_HOST = 'http://localhost:9200'

    # Act
    client = get_es_client()

    # Assert
    assert client is None
    mock_elasticsearch.assert_called_once_with(hosts=['http://localhost:9200'])
    mock_client.ping.assert_called_once()

@pytest.mark.django_db
@patch('ai_agent.shared_utils.es_client.Elasticsearch', side_effect=Exception("Connection Error"))
def test_get_es_client_exception(mock_elasticsearch):
    """
    Tests that get_es_client returns None when an exception occurs.
    """
    # Arrange
    settings.ELASTICSEARCH_HOST = 'http://localhost:9200'

    # Act
    client = get_es_client()

    # Assert
    assert client is None
    mock_elasticsearch.assert_called_once_with(hosts=['http://localhost:9200'])
