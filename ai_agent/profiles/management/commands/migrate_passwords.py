from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, identify_hasher
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Migrate existing user passwords to stronger hashing algorithms'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write('DRY RUN MODE - No changes will be made')
        
        # Get all users
        users = User.objects.all()
        migrated_count = 0
        skipped_count = 0
        
        for user in users:
            try:
                # Check if password needs migration
                hasher = identify_hasher(user.password)
                
                # If using an old hasher, migrate to new one
                # Check if the hasher has an algorithm attribute and if it's an old algorithm
                if hasattr(hasher, 'algorithm'):
                    algorithm = getattr(hasher, 'algorithm', '')
                    if algorithm in ['md5', 'sha1', 'unsalted_md5', 'unsalted_sha1']:
                        if not dry_run:
                            # Re-hash the password with the new algorithm
                            user.password = make_password(user.password)
                            user.save(update_fields=['password'])
                            logger.info(f"Migrated password for user: {user.username}")
                        
                        migrated_count += 1
                        self.stdout.write(
                            f"Would migrate password for user: {user.username}"
                            if dry_run else
                            f"Migrated password for user: {user.username}"
                        )
                    else:
                        skipped_count += 1
                        self.stdout.write(f"Skipped user {user.username} (already using modern hasher)")
                else:
                    skipped_count += 1
                    self.stdout.write(f"Skipped user {user.username} (hasher type not recognized)")
                    
            except Exception as e:
                self.stdout.write(f"Error processing user {user.username}: {str(e)}")
        
        self.stdout.write(
            f"\nMigration complete!\n"
            f"Migrated: {migrated_count} users\n"
            f"Skipped: {skipped_count} users\n"
            f"Total: {users.count()} users"
        ) 