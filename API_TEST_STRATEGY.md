# API Manual Test Strategy

This document outlines the testing strategy for the Microservices Mock Backend. The backend consists of three main endpoints: `POST /users`, `GET /users/{id}`, and `POST /checkout`. We use FastAPI with Pydantic for strict schema validation.

## 1. Endpoints & Features

| Endpoint | Method | Purpose | Key Validations |
|----------|--------|---------|-----------------|
| `/users` | POST | Creates a new user | Name length, Valid email format, Age limits (18-120). |
| `/users/{id}` | GET | Fetches an existing user | Existent/Non-existent ID check. |
| `/checkout` | POST | Submits an order | User existence, Quantity > 0, Flaky response (20% chance of 500 Error). |

## 2. Testing Scenarios

### A. Positive Flows (Happy Path)
1. **User Creation:**
   - **Action:** `POST /users` with valid payload (name="John Doe", email="john@example.com", age=30).
   - **Expected:** Status `201 Created`. Header `content-type: application/json`. Returns a valid UUID `id`.
2. **User Retrieval:**
   - **Action:** `GET /users/{id}` using the ID from step 1.
   - **Expected:** Status `200 OK`. The response JSON matches the payload submitted in step 1.
3. **Successful Checkout:**
   - **Action:** `POST /checkout` with the created `user_id`, a valid `item_id`, and `quantity` > 0.
   - **Expected:** Status `200 OK` (Assuming it doesn't hit the 20% flaky failure rate). Returns `status: "success"` and an `order_id`.

### B. Negative Flows & Validations

**POST /users:**
1. **Invalid JSON Format:**
   - **Action:** Send malformed JSON payload.
   - **Expected:** Status `422 Unprocessable Entity` or `400 Bad Request`.
2. **Missing Required Fields:**
   - **Action:** Omit `email` or `name` field.
   - **Expected:** Status `422 Unprocessable Entity` indicating the specific missing field.
3. **Boundary Testing (Age):**
   - **Action:** Send age as `17` or `121`.
   - **Expected:** Status `422 Unprocessable Entity`.
4. **Invalid Email Format:**
   - **Action:** Send `user.email = "not_an_email"`.
   - **Expected:** Status `422 Unprocessable Entity`.

**GET /users/{id}:**
1. **User Not Found:**
   - **Action:** `GET /users/invalid-or-unknown-uuid`.
   - **Expected:** Status `404 Not Found`.

**POST /checkout:**
1. **Invalid User ID:**
   - **Action:** Send `user_id` that doesn't exist in the system.
   - **Expected:** Status `404 Not Found` - "User not found for checkout".
2. **Zero or Negative Quantity:**
   - **Action:** Send `quantity: 0` or `quantity: -5`.
   - **Expected:** Status `422 Unprocessable Entity`.
3. **Flaky Integration / Timeout Simulation:**
   - **Action:** Repeatedly send valid `POST /checkout` requests (approx. 5-10 times).
   - **Expected:** Eventually, you should observe a `500 Internal Server Error` with details about a "Payment gateway timeout". This verifies the flaky third-party integration is simulated properly for retry-logic testing.

## 3. Headers and Metadata Testing
- Verify that response headers always contain `content-type: application/json`.
- Verify response times are within expected thresholds (locally < 50ms).

## 4. Test Environment Setup
- To start the server locally: `pip install -r requirements.txt && uvicorn app.main:app --reload`
- Swagger UI is available at `http://127.0.0.1:8000/docs` for quick documentation and manual execution.
- Use the provided Postman collection for automated schema and flow validation.
