# Spy Cat Agency (SCA)
## Overview
Spy Cat Agency (SCA) is a management application designed to simplify the process of managing spy cats, their missions, and targets. Built with FastAPI and SQLite, it provides RESTful APIs to handle CRUD operations for cats, missions, and targets.

## Features
### Spy Cats:
  - Create, update, delete, and list spy cats.
  - Validate cat breeds using TheCatAPI.
### Missions:
  - Create missions with associated targets.
  - Assign a cat to a mission
  - Mark missions and targets as complete.
  - Update mission targets or notes (unless completed).
  - Delete missions (only if not assigned to a cat).
  - List all missions or retrieve a single mission.
### Targets:
  - Unique within each mission.
  -Create, update, and mark as complete.

## Technologies Used
 - #### FastAPI
 - #### SQLAlchemy
 - #### SQLite
 - #### Alembic
 - #### TheCatAPI

## Getting Started
### Prerequisites
 - Python 3.8+
 - pip package manager
### Setup Instructions
1. Clone the Repository
```bash
git clone https://github.com/your-username/spy-cat-agency.git
```
2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate or  On Windows: venv\Scripts\activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run alembic migrations
```bash
alembic upgrade head
```
5. Run the Application
```bash
uvicorn main:app --reload
```
### API Documentation
You can access the API documentation at http://localhost:8000/docs
