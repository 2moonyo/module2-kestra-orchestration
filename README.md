# NYC Taxi Data Analysis with Docker & SQL

A beginner-friendly guide to loading and analyzing NYC Green Taxi data using Docker, PostgreSQL, and Python.

## What You'll Need

- Docker Desktop installed on your computer
- Basic terminal/command line knowledge

## Project Files

```
.
├── docker-compose.yml      # Defines PostgreSQL and pgAdmin containers
├── Dockerfile              # Defines the data ingestion container
├── Ingest_script.py        # Python script to load taxi data
├── pyproject.toml          # Python dependencies
└── README.md               # This guide
```

## Step-by-Step Guide

### Step 1: Start the Database

Open your terminal in this project folder and run:

```bash
docker-compose up -d
```

This starts two containers:
- **PostgreSQL** (database) - running on port `5432`
- **pgAdmin** (database UI) - running on port `8085`

Check if they're running:
```bash
docker ps
```

You should see containers named `pgdatabase` and `pgadmin`.

### Step 2: Access pgAdmin (Database UI)

1. Open your web browser and go to: **http://localhost:8085**

2. Login with these credentials:
   - **Email:** `admin@admin.com`
   - **Password:** `root`

3. Add a new server connection:
   - Right-click **"Servers"** → **"Register"** → **"Server"**
   - **General Tab:**
     - Name: `ny_taxi` (or any name you like)
   - **Connection Tab:**
     - Host: `pgdatabase`
     - Port: `5432`
     - Username: `root`
     - Password: `root`
     - Database: `ny_taxi`
   - Click **"Save"**

You're now connected to the database!

### Step 3: Build the Data Ingestion Container

This container will download and load the taxi data into PostgreSQL.

```bash
docker build -t taxi-ingestion .
```

This uses the **Dockerfile** to create an image named `taxi-ingestion`.

### Step 4: Load the Data

Run the container and get a bash terminal:

```bash
docker run -it --network module1_default taxi-ingestion
```

Inside the container, run the ingestion script:

```bash
uv run Ingest_script.py --pg-host=pgdatabase --pg-user=root --pg-pass=root
```

This will:
- Download NYC Green Taxi data for November 2025
- Download taxi zone lookup data
- Load everything into PostgreSQL

You'll see progress bars showing the download and ingestion status. When complete, you'll see: ✅ Data ingestion completed successfully!

Type `exit` to leave the container.

### Step 5: Verify Your Data

Go back to **pgAdmin** in your browser:

1. Expand: **Servers** → **ny_taxi** → **Databases** → **ny_taxi** → **Schemas** → **public** → **Tables**

2. You should see two tables:
   - `green_taxi` - Trip data
   - `taxi_zone` - Zone lookup data

3. Run a test query:
   - Right-click **ny_taxi** → **"Query Tool"**
   - Run this SQL:

```sql
SELECT COUNT(*) FROM green_taxi;
SELECT COUNT(*) FROM taxi_zone;
```

You should see thousands of taxi trips and 265 taxi zones!

## Quick Reference

### Container Configuration (docker-compose.yml)

- **PostgreSQL Service:** `pgdatabase`
  - Image: `postgres:18`
  - Port: `5432`
  - Username: `root`
  - Password: `root`
  - Database: `ny_taxi`

- **pgAdmin Service:** `pgadmin`
  - Port: `8085` (access via http://localhost:8085)
  - Email: `admin@admin.com`
  - Password: `root`

### Ingestion Script Options

You can customize the data ingestion:

```bash
uv run Ingest_script.py \
  --pg-host=pgdatabase \
  --pg-user=root \
  --pg-pass=root \
  --year=2025 \
  --month=11 \
  --green-table=green_taxi \
  --zone-table=taxi_zone \
  --chunksize=500
```

## Common Commands

**Check pip version in a Python container:**
```bash
docker run -it --entrypoint bash python:3.13
# Inside the container, run:
pip --version
# Exit with: exit
```

**Stop everything:**
```bash
docker-compose down
```

**Start again:**
```bash
docker-compose up -d
```

**Delete all data (reset):**
```bash
docker-compose down -v
```

**View container logs:**
```bash
docker logs pgdatabase
docker logs pgadmin
```

## Troubleshooting

**Can't access pgAdmin?**
- Make sure you're using `http://localhost:8085`
- Check if the container is running: `docker ps`

**Need to start over?**
```bash
docker-compose down -v
docker-compose up -d
# Then run ingestion again
```


