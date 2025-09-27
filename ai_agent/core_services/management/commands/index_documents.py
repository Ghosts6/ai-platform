import os
import logging
from django.core.management.base import BaseCommand, CommandError
from ai_agent.shared_utils.es_client import es_client
from elasticsearch.helpers import bulk

# Import new libraries for file parsing
import docx
from pypdf import PdfReader

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Indexes documents from a specified file or directory into Elasticsearch. Supports .txt, .docx, and .pdf files.'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='The path to the file or directory to index.')
        parser.add_argument(
            '--index_name',
            type=str,
            default='knowledge_base',
            help='The name of the Elasticsearch index to use. Defaults to \'knowledge_base\'.'
        )

    def handle(self, *args, **options):
        path = options['path']
        index_name = options['index_name']

        if not es_client:
            raise CommandError("Elasticsearch client is not available. Check your connection settings.")

        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f"Path '{path}' not found on the host. It must exist within the Docker container to be used with 'docker-compose exec'."))

        self.stdout.write(f"Starting to index documents from '{path}' into index '{index_name}'... (This path must be accessible inside the 'backend' container)")

        try:
            if not es_client.indices.exists(index=index_name):
                es_client.indices.create(index=index_name)
                self.stdout.write(self.style.SUCCESS(f"Created new index '{index_name}'"))

            success, failed = bulk(es_client, self._generate_actions(path, index_name))

            self.stdout.write(self.style.SUCCESS(f"Successfully indexed {success} documents (chunks)."))
            if failed:
                self.stderr.write(self.style.ERROR(f"Failed to index {len(failed)} documents."))

        except Exception as e:
            raise CommandError(f"An error occurred during indexing: {e}")

    def _generate_actions(self, path, index_name):
        """Yields actions for the Elasticsearch bulk helper from within the container."""
        if os.path.isdir(path):
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                if os.path.isfile(filepath):
                    yield from self._process_file(filepath, index_name)
        elif os.path.isfile(path):
            yield from self._process_file(path, index_name)

    def _process_file(self, filepath, index_name):
        """Reads a file, extracts text, chunks it, and yields Elasticsearch bulk actions."""
        self.stdout.write(f"Processing file: {filepath}")
        _, extension = os.path.splitext(filepath)
        content = ""

        try:
            if extension == '.txt':
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif extension == '.docx':
                doc = docx.Document(filepath)
                content = "\n".join([para.text for para in doc.paragraphs])
            elif extension == '.pdf':
                reader = PdfReader(filepath)
                content = "\n".join([page.extract_text() for page in reader.pages])
            else:
                self.stdout.write(self.style.WARNING(f"Skipping unsupported file type: {filepath}"))
                return

            # Simple chunking by paragraph
            chunks = content.split('\n\n')
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    doc = {
                        '_index': index_name,
                        '_source': {
                            'content': chunk.strip(),
                            'source_file': os.path.basename(filepath),
                            'chunk_id': i,
                        }
                    }
                    yield doc
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found inside the container: {filepath}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Could not process file {filepath}: {e}"))