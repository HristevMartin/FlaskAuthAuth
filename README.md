# Travel UB Application

## Overview
This is a travel application for management of travel passenger data. 

### Environment Variables
To set environment variables for the current session in Windows Command Prompt, use the following commands:
```cmd
set MONGO_HOST=localhost
set MONGO_PORT=27017
set MONGO_DB=travelDB
set SECRET_KEY=very_secret_token
```

## Setup and Installation
1. Clone the repository: `git clone <repo_link>`
2. Install the required packages: `pip install -r requirements.txt`
3. Run MongoDB in a container: `docker-compose up -d`
4. Run the application: `python app.py`
