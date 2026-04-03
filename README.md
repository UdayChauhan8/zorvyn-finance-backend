# Zorvyn Finance Data Processing and Access Control Backend

## 1. Project Overview
This project is a resilient, globally-structured RESTful API developed for the "Zorvyn FinTech" backend assignment. 
The application strictly enforces a **3-Tier Layered Architecture** perfectly separating concerns:
- **Routes (Controllers):** Handle HTTP traffic, intercept request JSON, utilize Marshmallow for input validation, and enforce JWT Role-Based Access Control via custom middlewares. They contain zero database logic.
- **Services:** Pure Python business logic layer. These files handle the heavy lifting (CRUD operations, math, dashboard calculations) by talking to the database. They contain zero HTTP routing logic.
- **Models / Database:** SQLAlchemy classes strictly mapped to relational database tables, enforcing Foreign Key constraints, data types, and timestamps.

This decoupling guarantees that the codebase is highly maintainable, testable, and scalable.

## 2. Tech Stack

| Technology | Purpose |
| ---------- | ------- |
| **Flask** | High-performance API routing and Python web server framework |
| **SQLAlchemy** | Strict Object Relational Mapper preventing raw SQL vulnerabilities |
| **SQLite** | Hassle-free file-based relational database (perfect for quick evaluations) |
| **Marshmallow**| Complex payload serialization, sanitization, and input validation |
| **JWT Extended** | Stateless authentication ensuring highly secure session tokenization |

## 3. Setup Instructions

To get the application running locally for evaluation, run the following commands sequentially:

```bash
# 1. Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 2. Install dependencies securely
pip install -r requirements.txt

# 3. Initialize the database and run the integrity Test Suite!
# This verifies the Models, Marshmallow Schemas, and bootstraps the zorvyn.db file
python test_state.py

# 4. Boot up the local development server (Runs on Port 5000)
python run.py
```

## 4. Role Matrix

The backend enforces strict Role-Based Access Control (RBAC) intercepting malicious payloads automatically.

| Action / Entity | Admin | Analyst | Viewer |
| --------------- | :---: | :-----: | :----: |
| **Auth System** | ✅ | ✅ | ✅ |
| **Dashboard Metrics**| ✅ | ✅ | ✅ |
| **View Transactions**| ✅ | ✅ | ✅ |
| **Create Transactions**| ✅ | ❌ | ❌ |
| **Edit Transactions**| ✅ | ❌ | ❌ |
| **Delete Transactions**| ✅ | ❌ | ❌ |

## 5. API Endpoints

### Auth
- `POST /api/auth/register` - Register a new User account
- `POST /api/auth/login` - Authenticate and retrieve a JWT Access Token
- `GET /api/auth/me` - Validates session and returns User Role dynamically

### Transactions
- `GET /api/transactions/` - Fetches global transactions. Supports query args: `?category=Salary&type=income&start_date=2026-01-01`
- `POST /api/transactions/` - Create a new financial record
- `PUT /api/transactions/<id>` - Modify a specific financial record
- `DELETE /api/transactions/<id>` - Soft-delete a transaction securely

### Dashboard
- `GET /api/dashboard/summary` - Generates Total Income, Total Expense, and Net Balance mathematically
- `GET /api/dashboard/category-breakdown` - Sum aggregation sliced horizontally by Categories
- `GET /api/dashboard/recent` - Rapidly fetches the last 5 active transactions globally

## 6. Technical Decisions & Trade-offs

During the architectural design phase, several careful decisions were made to build a production-emulated system while satisfying the exact requirements of the assignment constraints:

* **Soft Deletion Over Physical Deletion:** Instead of ever executing SQL `DELETE`, financial records contain an `is_deleted` column. Calling `.soft_delete()` flips this boolean and records a UTC timestamp `deleted_at`. This provides an invincible audit trail for the company.
* **SQLite Persistence:** While typically one configures Postgres or MySQL for finance, SQLite was strategically chosen here. It's fully relational and allows a Senior Engineer to simply pull this repo and run it instantly without spending 10 minutes configuring local Docker databases.
* **Centralized RBAC Middleware:** Rather than copying `if user.role != 'Admin'` in every single route, I authored a custom Python decorator (`@role_required`). Wrapping this over any endpoint guarantees mathematically that unauthorized users bounce with a `403 Forbidden` Exception before hitting the service logic.
* **Global Typed Error Handling:** Instead of writing massive `try/except` blocks in routing layers to spit out messy error strings, the app utilizes inherited `AppError` Exceptions. If the service layer raises `NotFoundError("Missing data")`, the central Flask config catches it blindly and generates a flawlessly formatted `{"error": "Missing data"}` string combined with the exact mapping HTTP block (Code `404`).
