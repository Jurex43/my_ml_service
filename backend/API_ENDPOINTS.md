# REST API Endpoints

## Base URL
All API endpoints are prefixed with: `http://localhost:8000/api/v1/`

## Available Endpoints

### 1. Endpoints
Manage ML service endpoints.

- **List all endpoints**: `GET /api/v1/endpoints/`
- **Retrieve specific endpoint**: `GET /api/v1/endpoints/{id}/`

**Allowed Methods**: GET (List, Retrieve only)

**Example Response**:
```json
{
  "id": 1,
  "name": "income_classifier",
  "owner": "admin",
  "created_at": "2026-05-16T10:00:00Z"
}
```

---

### 2. ML Algorithms
Manage machine learning algorithms.

- **List all algorithms**: `GET /api/v1/mlalgorithms/`
- **Retrieve specific algorithm**: `GET /api/v1/mlalgorithms/{id}/`

**Allowed Methods**: GET (List, Retrieve only)

**Example Response**:
```json
{
  "id": 1,
  "name": "Random Forest",
  "description": "Random Forest classifier for income prediction",
  "code": "rf_classifier.py",
  "version": "1.0.0",
  "owner": "admin",
  "created_at": "2026-05-16T10:00:00Z",
  "parent_endpoint": 1,
  "current_status": {
    "id": 1,
    "status": "production",
    "active": true,
    "created_by": "admin",
    "created_at": "2026-05-16T10:00:00Z"
  }
}
```

---

### 3. ML Algorithm Status
Manage the status of ML algorithms (e.g., testing, staging, production).

- **List all statuses**: `GET /api/v1/mlalgorithmstatuses/`
- **Retrieve specific status**: `GET /api/v1/mlalgorithmstatuses/{id}/`
- **Create new status**: `POST /api/v1/mlalgorithmstatuses/`

**Allowed Methods**: GET (List, Retrieve), POST (Create)

**Special Behavior**: 
- When creating a new status with `active=True`, all previous statuses for the same algorithm are automatically deactivated.
- This ensures only one status is active per algorithm at any time.

**Example POST Request**:
```json
{
  "status": "production",
  "active": true,
  "created_by": "admin",
  "parent_mlalgorithm": 1
}
```

---

### 4. ML Requests
Track prediction requests and responses.

- **List all requests**: `GET /api/v1/mlrequests/`
- **Retrieve specific request**: `GET /api/v1/mlrequests/{id}/`
- **Update request (add feedback)**: `PATCH /api/v1/mlrequests/{id}/`

**Allowed Methods**: GET (List, Retrieve), PATCH/PUT (Update)

**Example Response**:
```json
{
  "id": 1,
  "input_data": "{\"age\": 35, \"education\": \"Bachelors\"}",
  "full_response": "{\"prediction\": \">50K\", \"probability\": 0.85}",
  "response": ">50K",
  "feedback": "correct",
  "created_at": "2026-05-16T10:00:00Z",
  "parent_mlalgorithm": 1
}
```

**Example PATCH Request** (to add feedback):
```json
{
  "feedback": "correct"
}
```

---

## Running the Server

From the `backend` directory:

```bash
python manage.py runserver
```

Then visit:
- **API Root**: http://localhost:8000/api/v1/
- **Django Admin**: http://localhost:8000/admin/
- **Browsable API**: Available for all endpoints (DRF feature)

---

## Features

- **Pagination**: All list endpoints support pagination (10 items per page by default)
- **Filtering**: Use Django Filter backend for filtering results
- **Search**: Search functionality available on list endpoints
- **Ordering**: Order results by any field using `?ordering=field_name`
- **Browsable API**: Django REST Framework provides a web-browsable API interface

---

## Example Usage with curl

### List all endpoints
```bash
curl http://localhost:8000/api/v1/endpoints/
```

### Get specific algorithm
```bash
curl http://localhost:8000/api/v1/mlalgorithms/1/
```

### Create new algorithm status
```bash
curl -X POST http://localhost:8000/api/v1/mlalgorithmstatuses/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "production",
    "active": true,
    "created_by": "admin",
    "parent_mlalgorithm": 1
  }'
```

### Update ML request with feedback
```bash
curl -X PATCH http://localhost:8000/api/v1/mlrequests/1/ \
  -H "Content-Type: application/json" \
  -d '{"feedback": "correct"}'
```
