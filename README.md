# Export from Confluence Cloud

This repository contains a tool for backing up all pages from Confluence Cloud. With this tool, you can easily create local backups of your Confluence content for example.

## Installation

1. Clone this repository to your local machine:
    ~~~bash
    git clone https://github.com/csokolovsky/atlassian-cloud-backup.git
    ~~~
2. Navigate to the project directory:
    ~~~bash
    cd atlassian-cloud-backup
    ~~~
3. Install dependencies:
    ~~~bash
    pip install -r requirements.txt
    ~~~

## Usage

1. Configure your Confluence Cloud credentials and backup settings in the .env file.
   ~~~bash
   cp .env_example .env
   ~~~
2. Run the backup tool from the command line:
    ~~~bash
    python main.py
    ~~~

## Configuration

In the `.env` file, you can customize various settings:

- `ATLASSIAN_URL`: URL of your Atlassian Cloud. 
- `USERNAME`: Your Atlassian username.
- `TOKEN`: API token generated from your Atlassian account settings.
- `SPACE_KEY`: Confluence space to backup.
- `FORMAT`: Backup format pdf or word.

Example `.env`:
~~~
ATLASSIAN_URL="https://your_organization.atlassian.net"
USERNAME="your.email@example.com"
TOKEN="your_atlassian_token"
SPACE_KEY="MYSPACE"
FORMAT="pdf"
~~~

## Requirements

- Python 3.6+
- Pip (Python package manager)
- Requests library (automatically installed via `requirements.txt`)
