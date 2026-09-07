# Approval Workflow

A Django REST API for configurable, bilingual (English / Arabic) approval workflows. Requests move through statuses based on actions and transitions defined per request type — for example join requests, product updates, quantity increases, and customer information changes.

The domain is built around customers, products, committee/technical review, and a GFSA review step.

## Stack

- Python / Django 5.2
- Django REST Framework
- `django-cors-headers`
- SQLite (default; see `core/settings.py`)
- Custom user model: `requests.User`

## How it works

Each **request type** has an **approval workflow** with an initial status and a set of **transitions**. A transition is:

`from_status` + **action** → `to_status`

When a request is created, it is assigned a sequential number (`REQ-000001`) and the workflow’s initial status. Approving, rejecting, assigning committees, reopening, or applying a GFSA action looks up the matching transition and updates the request status.

### Request types

| Code | English | Arabic |
|------|---------|--------|
| `JOIN_REQUEST` | Join Request | طلب الانضمام |
| `UPDATE_PRODUCT_REQUEST` | Update Product Request | طلب تحديث المنتج |
| `CUSTOMER_CHANGE_INFO` | Customer Change Information | طلب تحديث بيانات العميل |
| `INCREASE_PRODUCT_REQUEST` | Increase Product Quantity Request | طلب زيادة كمية المنتج |

Join requests start at status **New** (code `1`). The other types start at **Branch Manager** (code `10`).

### Actions

`assign_committee`, `assign_technical`, `approve`, `reject`, `reopen`, `reassign_customer`, `reassign_committee`, `reassign_technical`, `reassign_both_committees`, `save_technical_form`, `save_committee_form`, `gfsa_action`

### Roles

Users (`requests.User`) have a role such as beneficiary, distributor, admin, branch manager, sales manager, CEO, committee member, technical member, or viewer.

## Project structure

```
core/                     # Django project (settings, URLs, WSGI/ASGI)
requests/                 # Requests domain (models, API, commands)
workflow/                 # Approval workflows, actions, transitions
  models/
  api/                    # DRF views, serializers, URLs
  services/               # Workflow, action, and transition services
scripts/                  # Seed data (types, statuses, actions, workflows, products)
postman/                  # Postman collection for API testing
manage.py
```

### Models

**requests app**

| Model | Purpose |
|-------|---------|
| `Request` / `RequestType` / `RequestStatus` | Request instance, kind, and current status |
| `RequestProduct` | Products and quantities on a request |
| `RequestSequence` | Sequential request numbering |
| `Customer` / `CustomerCategory` / `ApprovedProduct` | Customers and approved product quantities |
| `Product` | Catalog items |
| `CommitteeForm` / `TechnicalForm` | Review forms assigned to users |
| `User` | Custom `AbstractUser` with `role` |

**workflow app**

| Model | Purpose |
|-------|---------|
| `ApprovelWorkflow` | Workflow bound to a request type and initial status |
| `Action` / `Transition` | Allowed status moves |

Business logic lives in services:

- `workflow.services.approval_workflow_service.ApprovalWorkflowService` — resolve workflows and inspect graphs
- `workflow.services.transition_service.TransitionService` — create, update, and look up transitions
- `workflow.services.action_service.ActionService` — resolve actions
- `requests.services.requests_commands.RequestCommands` — create requests, generate numbers, GFSA bulk status update

## Setup

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

API bases:

- Requests: `http://127.0.0.1:8000/api/v1/requests/`
- Workflow: `http://127.0.0.1:8000/api/v1/workflow/`

There is no `requirements.txt` in the repo yet. Pin versions if you add one.

## Seed data

Reference data (request types, statuses, actions, workflows, products, customer categories, dummy customers) is loaded from Django shell:

```python
python manage.py shell
```

```python
from scripts.run_scripts import RunScripts
RunScripts().run()
```

To run a subset:

```python
RunScripts(scripts=["request_types", "request_statuses"]).run()
```

Available script keys: `request_types`, `request_statuses`, `products`, `customer_category`, `approval_actions`, `approval_workflows`.

Transitions are not seeded by `RunScripts`. Create them via the API or Django admin after workflows and actions exist.

## Testing the API (Postman)

Use the Postman collection in this repo to test the API:

[`postman/ApprovalWorkflow.postman_collection.json`](postman/ApprovalWorkflow.postman_collection.json)

1. Start the server (`python manage.py runserver`).
2. Seed data if you have not already (see **Seed data** above).
3. In Postman: **Import** → select `postman/ApprovalWorkflow.postman_collection.json`.
4. Confirm the collection variable `base_url` is `http://127.0.0.1:8000/api`.
5. Send requests from the **Requests** and **Workflow** folders.

The collection covers create request, apply approval, GFSA status update, get/list workflows, and create/update actions and transitions.

## API

### Requests (`/api/v1/requests/`)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/create` | Create a request (auto number + initial status) |
| `POST` | `/approval/create` | Apply an action and move the request to the next status |
| `PATCH` / `PUT` | `/update-gfsa-to-review-status` | Move requests in GFSA review (status `14`) to a random outcome (`7`, `9`, or `15`) |

### Workflow (`/api/v1/workflow/`)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/get?request_type=<CODE>` | Transitions for one request type |
| `GET` | `/list-all` | All workflows grouped by request type |
| `POST` | `/approval-create` | Create a workflow for a request type |
| `POST` | `/action/create` | Create an action |
| `POST` | `/transition/create` | Add a transition |
| `PUT` / `PATCH` | `/transition/update/<transition_id>` | Update a transition |

### Create request

```http
POST /api/v1/requests/create
Content-Type: application/json

{
  "type": "JOIN_REQUEST",
  "customer": 1,
  "products": [
    { "code": 101, "asked_quantity": 10 }
  ]
}
```

`customer` and `products` are optional. `type` is a request type **code**.

### Apply approval action

```http
POST /api/v1/requests/approval/create
Content-Type: application/json

{
  "request": 1,
  "action": "approve"
}
```

`action` is an `ActionType` value (for example `approve`, `reject`, `gfsa_action`). The request must have a unique matching transition from its current status.

### Create a transition

```http
POST /api/v1/workflow/transition/create
Content-Type: application/json

{
  "request_type": "JOIN_REQUEST",
  "from_status": 1,
  "to_status": 3,
  "action": "approve",
  "is_final": false
}
```

`from_status` and `to_status` are status **codes**. `is_final` marks a terminal step for that request type.

## CORS and auth

`corsheaders` is installed and middleware is enabled. CORS origins and REST Framework authentication are not configured in settings yet — treat this as a development setup. Authentication, permissions, and production secrets should be added before deployment.
