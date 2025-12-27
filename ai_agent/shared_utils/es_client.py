from elasticsearch import Elasticsearch, AsyncElasticsearch
from django.conf import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

def get_es_client():
    """
    Initializes and returns an Elasticsearch client instance.
    Returns None if the connection fails.
    """
    try:
        client = Elasticsearch(
            hosts=[settings.ELASTICSEARCH_HOST]
        )
        # Ping the server to verify the connection
        if not client.ping():
            logger.error("Failed to connect to Elasticsearch: Ping failed.")
            return None
        logger.info("Successfully connected to Elasticsearch.")
        return client
    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}", exc_info=True)
        return None

# A singleton instance for the application to use.
# This code will run once when the module is first imported.
es_client = get_es_client()
try:
    async_es_client = AsyncElasticsearch(
        hosts=[settings.ELASTICSEARCH_HOST]
    )
except Exception as e:
    logger.error(f"Error connecting to Elasticsearch: {e}", exc_info=True)
    async_es_client = None

