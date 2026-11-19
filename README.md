# Client CRM App

This is an internal CRM application for employees to manage client relationships and for logging client interactions.

## Project Status

### In development

The PostgreSQL database and FastAPI backend are in place. The React employee portal provides sign-in, a searchable client directory, and client record creation and editing.

## ⚡️Tech Stack

- 🐍Python
- 💨uv
- ⚡️FastAPI
- 🐘PostgresSQL
- React

## Planned Features

- Client record management
- Employee/user management
- Client interaction logging
- Interation types and history
- Authentication and authorization
- PostgreSQL database
- Internal deployment

## Development

This project uses uv for Python project and dependency management. Create the virtual environment and install dependencies with the command: **uv sync**

Run the backend and frontend in separate terminals:

```bash
./run_app.sh
```

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000` by default. To use a different backend URL, set `VITE_API_URL` before starting Vite, for example:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

Sign in with an employee account created for your deployment. The portal uses the backend's `/login/` and `/clients/` routes.

## Security

This repository contains application source code and configuration templates only.

Client information, employee credentials, API keys, database passwords, and other sensitive data must not be committed to the repository.