# Drone Dispatch Controller API

A REST API service for managing a fleet of drones capable of delivering medications. This system serves as a dispatch controller that allows clients to register drones, load them with medications, and monitor their status and battery levels.

## Project Overview

This application implements a drone dispatch system as specified in the Drones-v1-kata requirements:

- **Fleet Management**: Control up to 10 drones with different weight capacities
- **Medication Delivery**: Load drones with medication items for delivery
- **Battery Monitoring**: Continuous monitoring with automatic alerts when battery is low
- **State Management**: Track drone states (IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING)
- **Safety Controls**: Prevent overloading and loading when battery is below 25%

### Drone Models

- **Lightweight**: Lower capacity drones
- **Middleweight**: Medium capacity drones
- **Cruiserweight**: Higher capacity drones
- **Heavyweight**: Maximum capacity drones (up to 500gr)

## Prerequisites

- **Docker** (version 20.0 or higher)
- **Docker Compose** (version 2.0 or higher)

## Quick Start

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd hacktoberfest-api
```

### 2. Start All Services

```bash
docker-compose up -d
```

This command will:

- Start MongoDB database with persistent storage
- Build and start the FastAPI application
- Configure networking between services
- Expose API on port 8000

### 3. Verify Services

```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs api
docker-compose logs mongodb
```

### 4. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## Environment Configuration

The application uses environment-specific configurations:

### Docker Environment (`.env.docker`)

- **MongoDB**: `mongodb://root:hacktoberfest@mongodb:27017`
- **Database**: `drone_dispatch`
- **MQTT Broker**: Configured for external communication
- **API Port**: 8000

### Key Environment Variables

```bash
MONGODB_URL=mongodb://root:hacktoberfest@mongodb:27017
DATABASE_NAME=drone_dispatch
MQTT_BROKER=mqtt-broker
MQTT_PORT=1883
```

## API Endpoints

All endpoints return data in JSON format as required by the specifications.

### Drone Management

#### Register a Drone

```http
POST /api/v1/drones/
Content-Type: application/json

{
  "serial_number": "DRONE_001",
  "model": "Heavyweight",
  "weight_limit": 500,
  "battery_capacity": 100
}
```

**Response**: Registered drone object with state set to IDLE

#### Get Available Drones

```http
GET /api/v1/drones/available
```

**Response**: List of drones available for loading (IDLE state, battery > 25%)

#### Check Drone Battery

```http
GET /api/v1/drones/{serialNumber}/battery
```

**Response**: Current battery level for the specified drone

### Medication Management

#### Load Drone with Medications

```http
POST /api/v1/drones/{serialNumber}/load
Content-Type: application/json

[
  {
    "name": "Aspirin_500mg",
    "weight": 50.5,
    "code": "ASP_500",
    "image": "https://example.com/aspirin.jpg"
  }
]
```

**Response**: Updated drone object with loaded medications

#### Get Loaded Medications

```http
GET /api/v1/drones/{serialNumber}/medications
```

**Response**: List of medications currently loaded on the specified drone

## Data Models

### Drone

```json
{
  "serial_number": "string (max 100 chars)",
  "model": "Lightweight|Middleweight|Cruiserweight|Heavyweight",
  "weight_limit": "number (0-500gr)",
  "battery_capacity": "number (0-100%)",
  "state": "IDLE|LOADING|LOADED|DELIVERING|DELIVERED|RETURNING",
  "medications": []
}
```

### Medication

```json
{
  "name": "string (letters, numbers, -, _ only)",
  "weight": "number (>0)",
  "code": "string (uppercase letters, numbers, _ only)",
  "image": "string (valid URL)"
}
```

## Safety Features

The system implements several safety measures as required:

1. **Weight Validation**: Prevents loading drones beyond their weight limit
2. **Battery Protection**: Blocks loading when battery is below 25%
3. **State Management**: Enforces proper state transitions
4. **Automatic Monitoring**: Periodic battery checks with audit logging

## Battery Monitoring

The system includes automatic battery monitoring that:

- Checks all drone batteries every 30 seconds
- Creates audit logs for battery level changes
- Sends alerts when battery levels are critically low
- Prevents loading operations on low-battery drones

## Database

### MongoDB Setup

The application uses MongoDB for data persistence:

- **Container**: `mongodb` (mongo:latest)
- **Port**: 27017
- **Credentials**: root/hacktoberfest
- **Persistence**: Data stored in `mongo-data` volume

### Data Preloading

The system is designed to accept initial data through the API endpoints. No dummy data is preloaded by default, but you can populate the database using the registration endpoints.

## Development

### Project Structure

```
app/
 core/
    database.py          # MongoDB connection
    logger.py           # Logging configuration
 models/
    drone.py            # Drone data models
    medication.py       # Medication data models
 routes/
    drones.py           # Drone endpoints
    medications.py      # Medication endpoints
 services/
    drone_service.py    # Business logic
 main.py                 # FastAPI application
```

### Local Development

```bash
# Install dependencies
poetry install

# Run locally (requires local MongoDB)
poetry run uvicorn app.main:app --reload

# Run with Docker for consistency
docker-compose up
```


## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Use different port
docker-compose up -d --build --force-recreate
```

#### Database Connection Issues

```bash
# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

#### Build Issues

```bash
# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Health Checks

#### Verify API Health

```bash
curl http://localhost:8000/docs
```

#### Check Database Connection

```bash
docker-compose exec mongodb mongosh -u root -p hacktoberfest
```

#### Monitor Logs

```bash
# Follow API logs
docker-compose logs -f api

# Follow all logs
docker-compose logs -f
```

## Production Deployment

For production deployment:

1. **Environment Variables**: Update `.env.docker` with production values
2. **Security**: Change default MongoDB credentials
3. **Persistence**: Ensure volume backup strategy
4. **Monitoring**: Implement health checks and logging
5. **Scaling**: Consider load balancing for API service

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## API Documentation

For detailed API documentation with interactive examples, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The API follows OpenAPI 3.0 specifications and provides comprehensive documentation for all endpoints, request/response schemas, and error codes.
