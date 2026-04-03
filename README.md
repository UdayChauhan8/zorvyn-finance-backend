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

## 3. Live API Deployment

This API is currently proudly deployed and securely hosted live on the PythonAnywhere cloud infrastructure.

**Live Production Base URL:**
👉 **[https://udaychauhan8.pythonanywhere.com/](https://udaychauhan8.pythonanywhere.com/)**

*You can verify the system is running by hitting the [Health Check Endpoint](https://udaychauhan8.pythonanywhere.com/health) which natively returns a `200 OK` production payload.*

---

## 4. End-to-End API Testing (Postman)

To rigorously test the entire architecture (including Role Guards, Math Aggregations, and Error Handling constraints), a meticulously crafted Postman Collection has been published to a live Workspace.

You can instantly view and execute the entire 19-step test suite (from Token Generation to 403-Validation) via this public workspace link:
👉 **[Zorvyn Finance API Postman Tests](https://chauhanuday817-4305036.postman.co/workspace/TeamCache's-Workspace~658161fa-7250-4621-8c8c-469b1a09d791/collection/48586559-32ceca3e-c655-446f-883f-cfba7bb32007?action=share&creator=48586559&active-environment=48586559-07d03a73-b8f3-4977-84db-a87b5b222ea4)**

1. Simply open the workspace link above.
2. The folder contains fully sequenced tests verifying everything seamlessly.
3. *Important:* Ensure the environment selected in the top right is pointing the `base_url` to the live `pythonanywhere` server.

---

## 5. Local Setup Instructions

If you prefer to run the application dynamically on your own local machine for architectural evaluation, run the following commands sequentially:

```bash
# 1. Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 2. Install dependencies securely
pip install -r requirements.txt

# 3. Initialize the database and run the integrity Test Suite!
python test_state.py

# 4. Boot up the local development server (Runs on Port 5000)
python run.py
```

## 6. Role Matrix

The backend enforces strict Role-Based Access Control (RBAC) intercepting malicious payloads automatically.

| Action / Entity | Admin | Analyst | Viewer |
| --------------- | :---: | :-----: | :----: |
| **Auth System** | ✅ | ✅ | ✅ |
| **Dashboard Metrics**| ✅ | ✅ | ✅ |
| **View Transactions**| ✅ | ✅ | ✅ |
| **Create Transactions**| ✅ | ❌ | ❌ |
| **Edit Transactions**| ✅ | ❌ | ❌ |
| **Delete Transactions**| ✅ | ❌ | ❌ |

## 7. API Endpoints

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

## 8. Technical Decisions & Trade-offs

During the architectural design phase, several careful decisions were made to build a production-emulated system while satisfying the exact requirements of the assignment constraints:

* **Soft Deletion Over Physical Deletion:** Instead of ever executing SQL `DELETE`, financial records contain an `is_deleted` column. Calling `.soft_delete()` flips this boolean and records a UTC timestamp `deleted_at`. This provides an invincible audit trail for the company.
* **SQLite Persistence:** While typically one configures Postgres or MySQL for finance, SQLite was strategically chosen here. It's fully relational and allows a Senior Engineer to simply pull this repo and run it instantly without spending 10 minutes configuring local Docker databases.
* **Centralized RBAC Middleware:** Rather than copying `if user.role != 'Admin'` in every single route, I authored a custom Python decorator (`@role_required`). Wrapping this over any endpoint guarantees mathematically that unauthorized users bounce with a `403 Forbidden` Exception before hitting the service logic.
* **Global Typed Error Handling:** Instead of writing massive `try/except` blocks in routing layers to spit out messy error strings, the app utilizes inherited `AppError` Exceptions. If the service layer raises `NotFoundError("Missing data")`, the central Flask config catches it blindly and generates a flawlessly formatted `{"error": "Missing data"}` string combined with the exact mapping HTTP block (Code `404`).
