# db-postgre-sql

This component is responsible for deploying SQL scripts to a PostgreSQL database.

When a new SQL script is added to the db-scripts/ directory and ./main.py is executed, all pending scripts in the folder are applied to the target database.

🚀 How It Works

    Place your SQL files in the db-scripts/ directory.

    Test run the deployment tool: docker-compose up --build and python3 main.py

The tool connects to the configured PostgreSQL database and applies each script in order.
