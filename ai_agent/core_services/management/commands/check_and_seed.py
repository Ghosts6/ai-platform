from django.core.management.base import BaseCommand
from django.core import management
from ai_agent.shared_utils.es_client import es_client

class Command(BaseCommand):
    help = 'Checks if the knowledge_base index is empty and seeds it with initial data if necessary.'

    def handle(self, *args, **options):
        if not es_client:
            self.stdout.write(self.style.ERROR("Elasticsearch not available. Skipping knowledge base seeding."))
            return

        index_name = 'knowledge_base'
        try:
            # Check if index exists and has documents
            if not es_client.indices.exists(index=index_name) or es_client.count(index=index_name)['count'] == 0:
                self.stdout.write(self.style.WARNING(f"Knowledge base index '{index_name}' is missing or empty. Seeding initial data..."))
                # Call the index_documents command
                management.call_command('index_documents', '/app/ai_agent/data')
                self.stdout.write(self.style.SUCCESS("Successfully seeded knowledge base."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Knowledge base '{index_name}' already contains data. Skipping seeding."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred while checking or seeding the knowledge base: {e}"))
