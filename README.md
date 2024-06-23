# FastAPI with SQLModel and Alembic for PostgreSQL Migrations

This project demonstrates how to set up a FastAPI application using SQLModel with a PostgreSQL database and handle database migrations using Alembic in a separate Docker container.

## Project Structure

```
api/
├── __init__.py
├── models.py
├── migration_service/
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── env.py
│   ├── requirements.txt
│   ├── entrypoint.sh
│   └── versions/
└── docker-compose.yml
```

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### Step 1: Build and Run the Docker Containers

Build and start the services defined in the `docker-compose.yml` file:

```bash
docker-compose up --build
```

### Step 2: Project Dependencies

Ensure you have the necessary dependencies listed in the `requirements.txt` for both the FastAPI app and the migration service.

#### migration_service/requirements.txt

```txt
alembic
psycopg2
sqlmodel
```

### Step 3: Alembic Configuration

#### migration_service/alembic.ini

Update the `alembic.ini` file with your database connection string:

```ini
sqlalchemy.url = postgresql+psycopg2://username:password@db/mydatabase
```

#### migration_service/env.py

Ensure your models are imported correctly in `env.py`:

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context

config = context.config
fileConfig(config.config_file_name)

from app.models import MyModel1, MyModel2  # Import your models here

target_metadata = SQLModel.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Step 4: Entrypoint Script

#### migration_service/entrypoint.sh

Create an entrypoint script to handle the migration process:

```bash
#!/bin/bash

# Wait for the database to be available
while ! nc -z db 5432; do
  echo "Waiting for database..."
  sleep 1
done

# Run Alembic migrations
alembic upgrade head

echo "Database migration completed."
```

### Step 5: Create and Apply Migrations

Whenever you make changes to your models, follow these steps:

1. **Generate a new migration script:**

   ```bash
   docker-compose run migration alembic revision --autogenerate -m "Describe your changes"
   ```

2. **Apply the migration:**

   ```bash
   docker-compose run migration alembic upgrade head
   ```

## Running the FastAPI Application

The FastAPI application will be accessible at `http://localhost:8000`.

### Example FastAPI Endpoint

```python
from fastapi import FastAPI
from sqlmodel import SQLModel, Field

app = FastAPI()

class MyModel1(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
```

## License

This project is licensed under the MIT License.
