# Organization Management Service (FastAPI + MongoDB)

## Overview
This project implements a multi-tenant organization management backend using **FastAPI** and **MongoDB**.  
It keeps a **Master DB** (metadata + admin credentials) and creates **dynamic collections** per organization (pattern `org_<organization_name>`).

### Features
- `POST /org/create` — Create organization and admin; creates tenant collection.
- `GET /org/get?organization_name=...` — Fetch org metadata.
- `PUT /org/update` — Update org (rename optionally with data migration) and admin details.
- `DELETE /org/delete` — Delete org (admin-authenticated).
- `POST /admin/login` — Admin login returns JWT containing `admin_id` and `org_id`.

## Project layout
