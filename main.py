#!/usr/bin/env python

import os
from atlassian import Confluence
import sqlite3
import logging
from dotenv import load_dotenv
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_objects (
            id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()


def save_processed_object(conn, obj_id):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO processed_objects (id) VALUES (?)', (obj_id,))
    conn.commit()


def load_processed_objects(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM processed_objects')
    return [row[0] for row in cursor.fetchall()]


def export_page_pdf(page, confluence):
    response = confluence.get_page_as_pdf(page_id=page['id'])
    save_file(response, page['title'], 'pdf')


def export_page_word(page, confluence):
    response = confluence.get_page_as_word(page_id=page['id'])
    save_file(response, page['title'], 'doc')


def save_file(content, title, extension):
    s_title = replace_forbidden_chars(title, r'[/]')
    with open(s_title + '.' + extension, 'wb') as f:
        f.write(content)
        f.close()
        logger.info('File saved')


def replace_forbidden_chars(text, forbidden_chars, replacement='-'):
    pattern = re.compile(forbidden_chars)
    return re.sub(pattern, replacement, text)


def main():
    load_dotenv()

    conn = sqlite3.connect('processed_objects.db')
    create_table_if_not_exists(conn)
    processed_objects = load_processed_objects(conn)

    backup_format = os.getenv('FORMAT')

    try:
        confluence = Confluence(
            url=os.getenv('ATLASSIAN_URL'),
            username=os.getenv('USERNAME'),
            password=os.getenv('TOKEN'),
            api_version='cloud',
            cloud=True
        )

        pages = confluence.get_all_pages_from_space(
            space=os.getenv('SPACE_KEY'),
            start=0,
            limit=1500,
            status=None,
            expand=None,
            content_type="page"
        )

        for page in pages:
            logger.info(f'Page export started: {page["title"]}')
            if int(page['id']) in processed_objects:
                logger.info('Page already dumped')
                continue

            if backup_format == 'pdf':
                export_page_pdf(page, confluence)
            else:
                export_page_word(page, confluence)

            save_processed_object(conn, page['id'])
    except Exception as e:
        logger.error(e)
    finally:
        conn.close()


if __name__ == '__main__':
    logging.info('Started app')
    main()