# Patient Data Retrieval API

A Flask-based REST API for retrieving and managing patient medical data. The API provides endpoints for querying patient data across different tables and returns the results in FHIR v5 format.

## Project Structure

```
PatientDataRetriever_v3-4/
├── app/                    # Main application code
├── docs/                   # Documentation files
│   ├── examples/          # Example API responses
│   │   ├── valid/        # Valid response examples
│   │   └── invalid/      # Invalid response examples
│   └── static/           # Static documentation files
├── sql/                   # SQL scripts and database-related files
├── static/               # Static files for the web application
├── tests/                # Test suite
├── Dockerfile            # Docker configuration for the application
├── docker-compose.yml    # Docker Compose configuration
├── main.py              # Application entry point
├── requirements.txt     # Python package dependencies with versions
├── requirements_package_names_only.txt  # Package names without versions
├── setup_postgres_container.sh         # PostgreSQL container setup script
└── docker_rebuild_container_from_scratch.sh  # Docker rebuild script
```

## Features

- RESTful API endpoints for patient data retrieval
- Secure authentication system with role-based access control
- Support for multiple medical data tables (vital signs, lab results, etc.)
- Combined vital signs query capability using optimised UNION ALL queries
  - Performance improvements of up to 60-70% compared to individual queries
  - Reduced database load and network traffic
- FHIR v5 formatted responses with consistent resource IDs
- Comprehensive data validation
- Docker support for easy deployment
- PostgreSQL database integration
- Swagger UI documentation

## Available Tables

The API supports querying from the following table categories:

### Core Vital Signs
- `saturacion_oxigeno` - Oxygen saturation measurements
- `temperatura` - Body temperature readings
- `presion_arterial` - Blood pressure measurements
- `frecuencia_cardiaca` - Heart rate readings
- `frecuencia_respiratoria` - Respiratory rate readings
- `constantes` - Combined vital signs

### Clinical Measurements
- `glucosa` - Blood glucose readings
- `peso` - Weight measurements
- `talla` - Height measurements
- `diuresis` - Urine output tracking
- `deposiciones` - Bowel movement tracking
- `electrocardiograma` - ECG readings

### Clinical Events
- `medicacion` - Medication administration records
- `ulceras` - Pressure ulcer documentation
- `contencion` - Patient restraint records
- `tipo_sonda` - Tube/catheter documentation

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Docker and Docker Compose (optional, for containerised deployment)

## Installation

### Local Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd PatientDataRetriever_v3-4
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   ./setup_postgres_container.sh
   ```
   This script:
   - Stops and removes any existing PostgreSQL container named 'km0-postgres'
   - Creates a new PostgreSQL 16.6 container with the following configuration:
     - Exposes port 5432 for database connections
     - Sets up the database password as 'admin'
     - Creates a database named 'KM0'
     - Configures the container to restart automatically unless stopped manually
   - Provides instructions for restoring data from a backup file

5. Run the application:
   ```bash
   python main.py
   ```

### Docker Installation

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

2. To rebuild from scratch:
   ```bash
   ./docker_rebuild_container_from_scratch.sh
   ```
   This script performs a complete rebuild of the Docker environment by:
   - Stopping all running containers and removing orphaned containers
   - Rebuilding all images from scratch without using cache
   - Starting the containers in detached mode
   This is useful when you need to ensure a completely fresh build of the environment.

## Authentication

The API uses a secure authentication system with role-based access control. All endpoints except metadata endpoints require authentication.

### Authentication Flow

1. Obtain a JWT token by authenticating with the `/api/auth/login` endpoint
2. Include the token in subsequent requests using the `Authorization` header
3. The token will be validated for each request
4. Access to certain endpoints may be restricted based on user roles

### Authentication Endpoint

#### POST /api/auth/login

Authenticate a staff member using a secure POST request. Credentials must be sent in the request body for security reasons.

Request body format:
```json
{
    "username": "Emma",
    "usersurname": "Wilson",
    "password": "EmmaW2024!"
}
```

Response format:
```json
{
    "success": true,
    "role": "medical",
    "token": "Bearer eyJhbGciOiJIUzI1NiIs...",
    "message": "Authentication successful. Use the token in the Authorization header as: Bearer {token}"
}
```

**Security Note**: 
- Authentication is only available via POST to ensure credentials are not exposed in URLs, logs, or browser history
- Tokens expire after a configurable period (default: 24 hours)
- Failed authentication attempts are logged for security monitoring

## Documentation Structure

The API documentation is organised as follows:

- `docs/static/`: Contains static documentation files including:
  - `openapi.yaml`: OpenAPI/Swagger specification file that describes:
    - API endpoints
    - Request/response formats
    - Data models
    - Field validations
    - Example requests

- `docs/examples/`: Directory containing JSON examples of API responses:
  - `docs/examples/valid/`: Valid response examples:
    - [`valid_response_model.json`](docs/examples/valid/valid_response_model.json): Standard valid response model
    - [`valid_response_case_study_short_dt_range.json`](docs/examples/valid/valid_response_case_study_short_dt_range.json): Case study with a short date range
    - [`valid_response_case_study_longer_dt_range.json`](docs/examples/valid/valid_response_case_study_longer_dt_range.json): Case study with a longer date range
  - `docs/examples/invalid/`: Invalid response examples:
    - [`invalid_response_model.json`](docs/examples/invalid/invalid_response_model.json): Example of an invalid response structure

- `sql/`: Contains SQL scripts and database-related files for:
  - Database schema definitions
  - Migration scripts
  - Query templates
  - Database maintenance scripts

- `static/`: Contains static files for the web application:
  - CSS stylesheets
  - JavaScript files
  - Images and other static assets

## Accessing the API Documentation

The API documentation is available in two formats:

1. **Swagger UI** (Interactive Documentation):
   - Local: `http://localhost:5012/docs`
   - Docker: `http://localhost:5009/docs`

2. **OpenAPI Specification**:
   - View the raw specification in `docs/static/openapi.yaml`
   - Import into tools like Postman or Swagger Editor

## API Endpoints

### 1. GET /api/metadata/api
Returns general API documentation and usage information.

### 2. GET /api/metadata/vital_signs
Returns metadata for vital signs tables and fields.

### 3. GET /api/metadata/operational_data
Returns metadata for operational data tables and fields.

### 4. POST /api/vital_signs/query
Query patient vital signs data for all vital sign tables using a JSON request body.

Request body format:
```json
{
    "id_patient": "0000021561",
    "date_range": {
        "min_date": "2024-03-01",
        "max_date": "2024-03-31 23:59"
    }
}
```

### 5. GET /api/vital_signs/{id_value}/{min_date}/{max_date}
Retrieve all vital signs data for a patient within a date range.

Parameters:
- `id_value`: Patient ID value
- `min_date`: Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)
- `max_date`: End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)

### 6. GET /api/operational_data/{id_value}/{min_date}/{max_date}
Retrieve operational data for a patient within a date range (admin only).

Parameters:
- `id_value`: Patient ID value (format: 0000021561)
- `min_date`: Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)
- `max_date`: End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)

Example:
```
GET /api/operational_data/0000021561/2024-03-01/2024-03-31 23:59
```

### 7. POST /api/operational_data/query
Query operational data for a patient (admin only).

Request body format:
```json
{
    "id_patient": "0000021561",
    "date_range": {
        "min_date": "2024-03-01",
        "max_date": "2024-03-31 23:59"
    }
}
```

## Data Models

The API uses several data models:

1. **Documentation Model**:
   - Provides comprehensive API documentation
   - Includes available fields, value ranges, and operations
   - Used in GET /api/retrieve_data response

2. **Patient Query Model**:
   - Structure for querying patient records
   - Fields:
     - `table_name`: Name of the table to query
     - `id_patient`: Patient ID value
     - `date_range`: Date range parameters
   - Used in POST /api/retrieve_data request

3. **Response Model**:
   - Standardised response format
   - Fields:
     - `data`: Array of FHIR v5 Bundle resources containing patient observations
     - `count`: Number of records found

4. **Error Models**:
   - Schema Validation Error
   - Value Validation Error
   - Database Error
   - Server Error

## Response Format

### Success Response
```json
{
    "data": [
        {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [
                {
                    "resourceType": "Observation",
                    "id": "oxsat-1",
                    "status": "final",
                    "category": [
                        {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                    "code": "vital-signs",
                                    "display": "Vital Signs"
                                }
                            ]
                        }
                    ],
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "59408-5",
                                "display": "Oxygen saturation in Blood"
                            }
                        ]
                    },
                    "subject": {
                        "reference": "Patient/0000021561"
                    },
                    "effectiveDateTime": "2024-03-14T12:00:00",
                    "valueQuantity": {
                        "value": 98.5,
                        "unit": "%",
                        "system": "http://unitsofmeasure.org",
                        "code": "%"
                    }
                }
            ]
        }
    ],
    "count": 1
}
```

### Error Responses

1. Schema Validation Error (400):
   ```json
   {
       "field": "table_name",
       "error": "Invalid table name or field not supported for date filtering"
   }
   ```

2. Value Validation Error (400):
   ```json
   {
       "field": "date_field",
       "error": "Invalid date format. Must be YYYY-MM-DD or YYYY-MM-DD HH:MM"
   }
   ```

3. Database Error (500):
   ```json
   {
       "field": "database",
       "error": "Database error message"
   }
   ```

4. Server Error (500):
   ```json
   {
       "field": "server",
       "error": "Internal server error occurred"
   }
   ```

## Resource Prefixes

To ensure consistent and meaningful resource IDs, each table has a defined prefix for FHIR resource identifiers:

- `oxsat` - Oxygen saturation measurements (saturacion_oxigeno)
- `temp` - Body temperature readings (temperatura)
- `bp` - Blood pressure measurements (presion_arterial)
- `hr` - Heart rate readings (frecuencia_cardiaca)
- `rr` - Respiratory rate readings (frecuencia_respiratoria)
- `vitals` - Combined vital signs (constantes)
- `gluc` - Blood glucose readings (glucosa)
- `wt` - Weight measurements (peso)

## Date Format Validation

The API supports two date formats:
- `YYYY-MM-DD` (e.g., "2024-03-01")
  - When only date is provided:
    - For `min_value`: time defaults to 00:00
    - For `max_value`: time defaults to 23:59
- `YYYY-MM-DD HH:MM` (e.g., "2024-03-01 14:30")
  - Explicit time specification

## Port Configuration

- API Server: 
  - Docker: 5009 (host) → 5010 (container)
  - Local: 5013
- Database: PostgreSQL on port 5432 (configured in docker-compose.yml)
- Swagger UI: Available at /docs endpoint

When running locally without Docker, visit `http://localhost:5013/docs` for the Swagger UI.
When running with Docker, visit `http://localhost:5010/docs`.

For detailed field descriptions, validation rules, and example requests, please refer to the Swagger UI documentation.

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

The project follows PEP 8 style guidelines. Use the following tools to maintain code quality:

```bash
# Install development dependencies
pip install -r requirements.txt

# Run linting
flake8 .

# Run type checking
mypy .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.