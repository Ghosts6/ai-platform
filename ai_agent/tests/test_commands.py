
import pytest
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.core.management.base import CommandError
import os

@pytest.mark.django_db
@patch('ai_agent.core_services.management.commands.index_documents.es_client')
def test_index_documents_command_no_path(mock_es_client):
    """
    Tests that the command raises an error if no path is provided.
    """
    with pytest.raises(CommandError):
        call_command('index_documents')

from ai_agent.core_services.management.commands.index_documents import Command

@pytest.mark.django_db
@patch('ai_agent.core_services.management.commands.index_documents.es_client')
def test_index_documents_command_handle(mock_es_client):
    # Arrange
    command = Command()
    command.stdout = MagicMock()
    command.stderr = MagicMock()
    mock_es_client.indices.exists.return_value = True
    with patch('os.path.exists') as mock_exists, \
         patch('os.path.isdir') as mock_isdir, \
         patch('os.listdir') as mock_listdir, \
         patch('os.path.isfile') as mock_isfile, \
         patch('builtins.open') as mock_open, \
         patch('ai_agent.core_services.management.commands.index_documents.bulk') as mock_bulk:

        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_listdir.return_value = ['test.txt']
        mock_isfile.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = "This is a test."
        mock_bulk.return_value = (1, [])

        # Act
        command.handle(path='fake_path', index_name='knowledge_base', verbosity=1)

        # Assert
        mock_es_client.indices.exists.assert_called_once_with(index='knowledge_base')
        mock_bulk.assert_called_once()
