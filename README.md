# Pawfound API

Pawfound is a Flask REST API for a pet-adoption platform. It lets adopters browse pets and shelters, save favourites, and submit adoption requests. Administrators can manage shelters and pets, and review adoption requests.

## Tech stack

Python 3.12
Flask
Flask-SQLAlchemy with SQLite
Flask-Migrate
Flask-JWT-Extended for authentication and authorization
Flask-Bcrypt for password hashing
Flask-CORS

## Getting started

### Pre-requisites

- Python 3.12
- [Pipenv](https://pipenv.pypa.io/)

### Installation

```bash
git clone <repository-url>
cd back_end
pipenv install
```

Set a JWT secret before starting the app. The fallback value in `config.py` is only suitable for local development.

```bash
export JWT_SECRET_KEY="replace-with-a-long-random-secret-key"
```

Create the database from the included migrations, then optionally load sample data:

```bash
pipenv run flask --app app db upgrade
pipenv run python seed.py
```

> **Note:** `seed.py` deletes existing pets, shelters, and users before adding sample data. Use it only when resetting local development data.

### Run the API

```bash
pipenv run python app.py
```

The server starts at `http://127.0.0.1:5000` in debug mode. Confirm it is running with:

```bash
curl http://127.0.0.1:5000/
```

Expected response:

```json
{"message": "Pawfound API running"}
```

## Authentication and roles

Register with `POST /auth/register`, then log in using `POST /auth/login`. Successful login returns an access token. Send it for protected routes:

```http
Authorization: Bearer <access_token>
```

Users default to the `adopter` role. Routes that create, update, delete, or review platform records require an `admin` token.

When the sample data is loaded, these accounts are available:

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@pawfound.com` | `admin123` |
| Adopter | `joel@example.com` | `password123` |
| Adopter | `mary@example.com` | `password123` |

These credentials are for local development only.

## API reference

All requests and responses use JSON unless otherwise indicated.

### Authentication

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| POST | `/auth/register` | Public | Create a user. |
| POST | `/auth/login` | Public | Obtain a JWT access token. |
| GET | `/auth/profile` | Authenticated | View the current user's profile. |

Register request body:

```json
{
  "username": "alex",
  "email": "alex@example.com",
  "password": "secure-password",
  "role": "adopter"
}
```

Login request body:
```json
{
  "email": "alex@example.com",
  "password": "secure-password"
}
```

### Pets
| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| GET | `/view-all-pets` | Public | List all pets. |
| GET | `/pet/<id>` | Public | Retrieve one pet. |
| POST | `/add-pet` | Admin | Create a pet. |
| PATCH / PUT | `/pet/<id>` | Admin | Update a pet. |
| DELETE | `/pet/<id>` | Admin | Delete a pet. |

Create-pet request body:
```json
{
  "name": "Bella",
  "species": "Dog",
  "breed": "German Shepherd",
  "age": 2,
  "gender": "female",
  "image_url": "https://example.com/bella.jpg",
  "shelter_id": 1
}
```

Pets start with the status `available`. An admin may update fields such as `name`, `species`, `breed`, `age`, `gender`, `image_url`, `shelter_id`, and `status`.

### Shelters

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| GET | `/view-all-shelters` | Public | List shelters. |
| GET | `/view-shelter/<id>` | Public | Retrieve one shelter. |
| POST | `/add-shelter` | Admin | Create a shelter. |
| PATCH | `/shelter/<id>` | Admin | Update a shelter. |
| DELETE | `/shelter/<id>` | Admin | Delete a shelter without assigned pets. |

Create-shelter request body:
```json
{
  "name": "Happy Paws Shelter",
  "email": "hello@happypaws.example",
  "address": "123 Main Street",
  "city": "Nairobi",
  "phone": "0711111111"
}
```

### Favourites

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| POST | `/add-favourite` | Authenticated | Add a pet to the current user's favourites. |
| GET | `/my-favourites` | Authenticated | List the current user's favourite pets. |
| DELETE | `/remove-favourite/<pet_id>` | Authenticated | Remove a favourite. |

Add-favourite request body:
```json
{"pet_id": 1}
```

### Adoption requests

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| POST | `/adoption-request` | Adopter | Submit a request for an available pet. |
| GET | `/my-adoption-requests` | Authenticated | List the current user's requests. |
| GET | `/adoption-requests` | Admin | List every adoption request. |
| PATCH | `/adoption-request/<request_id>` | Admin | Set a request to `Approved`, `Rejected`, or `Pending`. |

Submit-request body:
```json
{
  "pet_id": 1,
  "notes": "I have a secure yard and experience with dogs."
}
```

Approving a request updates that pet's status to `adopted`.

## Database migrations

After changing SQLAlchemy models, create and apply a migration:

```bash
pipenv run flask --app app db migrate -m "describe the change"
pipenv run flask --app app db upgrade
```

The local SQLite database is stored at `instance/pawfound.db`.

## Project structure

```text
back_end/
├── app.py              # Application factory setup and blueprint registration
├── config.py           # SQLite and JWT configuration
├── extensions.py       # Shared Flask extension instances
├── models/             # SQLAlchemy models and relationships
├── routes/             # Authentication, pets, shelters, favourites, and requests
├── migrations/         # Flask-Migrate/Alembic migration files
└── seed.py             # Local development sample data
```
