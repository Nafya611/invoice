# Invoice Project

This project is a FastAPI-based application that connects to a MySQL database for managing clients and invoices.

## Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose
- MySQL 8.0
- Git

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Nafya611/invoice.git
   cd invoice
   ```

2. **Set Up MySQL Database**
   Ensure Docker is installed and running. Use the following `docker-compose.yml` file:
   ```yaml
   version: '3.8'

   services:
     db:
       image: mysql:8.0
       container_name: mysql-db
       restart: always
       environment:
         MYSQL_ROOT_PASSWORD: "tobefilled"
         MYSQL_DATABASE: my_database
         MYSQL_PASSWORD: tobefilled
       ports:
         - "3306:3306"
       volumes:
         - mysql-data:/var/lib/mysql

   volumes:
     mysql-data:
   ```
   Run the following command to start the database:
   ```bash
   docker-compose up -d
   ```

3. **Install Python Dependencies**
   Ensure Python 3.13 is installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not available, install the following manually:
   ```bash
   pip install fastapi uvicorn sqlalchemy pymysql cryptography
   ```

## Running the Application

1. **Start the FastAPI Application**
   Run the following command:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the Application**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

3. **API Endpoints**
   - `/clients`: Get all clients.
   - `/invoices/client?client_name=<name>`: Get invoices for a specific client.

## Notes

- Ensure the MySQL database is running before starting the FastAPI application.
- Update the connection string in `main.py` if the database credentials or host change.

## License

This project is licensed under the MIT License.
