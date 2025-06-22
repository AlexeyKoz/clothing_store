#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def create_productlike_table():
    """Create the catalog_productlike table manually"""
    with connection.cursor() as cursor:
        # Create the table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS catalog_productlike (
                id BIGSERIAL PRIMARY KEY,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                product_id BIGINT NOT NULL,
                user_id INTEGER NOT NULL,
                CONSTRAINT catalog_productlike_user_id_product_id_key UNIQUE (user_id, product_id),
                CONSTRAINT catalog_productlike_product_id_fkey FOREIGN KEY (product_id) REFERENCES catalog_product(id) DEFERRABLE INITIALLY DEFERRED,
                CONSTRAINT catalog_productlike_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
            );
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS catalog_productlike_product_id ON catalog_productlike (product_id);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS catalog_productlike_user_id ON catalog_productlike (user_id);
        """)
        
        print("Successfully created catalog_productlike table")

def mark_migration_as_applied():
    """Mark the catalog.0002_productlike migration as applied"""
    with connection.cursor() as cursor:
        # Check if migration already exists
        cursor.execute("""
            SELECT COUNT(*) FROM django_migrations 
            WHERE app = 'catalog' AND name = '0002_productlike';
        """)
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('catalog', '0002_productlike', NOW());
            """)
            print("Successfully marked catalog.0002_productlike as applied")
        else:
            print("Migration catalog.0002_productlike already marked as applied")

if __name__ == '__main__':
    try:
        create_productlike_table()
        mark_migration_as_applied()
        print("Migration issue fixed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 