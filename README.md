# FilmSearch — Algorithmics Movies Project

A Django 4 web app for discovering movies: search by rich filters, view details, track your watch history, and get personalized recommendations.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Data Model](#data-model)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Run the app](#run-the-app)
  * [Create an admin user](#create-an-admin-user)
* [Key URLs](#key-urls)
* [Searching & Sorting](#searching--sorting)
* [Recommendations](#recommendations)

---

## Overview

**FilmSearch** helps movie lovers explore and manage their viewing: browse top‑rated films, search by multiple criteria, open a movie detail page, mark films as watched (with a like/neutral/dislike rating), and receive personalized recommendations based on your watch history and preferences.

The project is organized into two Django apps:

* **`movies`** — core catalog (models, search, listing, details)
* **`users`** — authentication, profile, watch history, and recommendations

---

## Features

* 🔍 **Advanced search** by title, release year, genre, director, actor, and age certificate (G/PG/PG‑13/R/NC‑17)
* 🏆 **Top‑rated movies** page
* 📄 **Movie detail** page
* ✅ **Watch tracking**: mark movies as watched and rate them (Liked/Neutral/Disliked)
* 🎯 **Personal recommendations** derived from your watch history
* 👶 **Kid‑friendly picks** (based on age certificates)
* 🆕 **Recently released highlights** (e.g., after 2016)
* 🧑‍💻 Admin UI for managing data (Django admin)
* 🎨 Bootstrap‑powered templates for a clean UI

---

## Tech Stack

* **Framework:** Django **4.2**
* **Python:** 3.10+ recommended
* **Database:** SQLite (local dev, `db.sqlite3` included)
* **Frontend:** Django templates with **Bootstrap 5**

Python dependencies (from `requirements.txt`):

```
asgiref==3.8.1
Django==4.2
sqlparse==0.5.3
typing_extensions==4.12.2
tzdata==2024.2
```

---

## Project Structure

```
Algorithmics-Movies-Project-master/
├─ algorithmics_project/           # Project settings, URLs, WSGI/ASGI
│  ├─ settings.py
│  └─ urls.py                      # Routes: index, admin, include(movies, users)
├─ movies/                         # Catalog app
│  ├─ models.py                    # Movie, Genre, Director, Star
│  ├─ forms.py                     # MovieSearchForm (filters & certificates)
│  ├─ urls.py                      # /movies/ endpoints (search, top-rated, detail)
│  └─ views.py                     # List/Detail/Search/Watch handling
├─ users/                          # User/Recommendations app
│  ├─ models.py                    # UserProfile, MovieWatch
│  ├─ views.py                     # Index, profile, recommendations
│  ├─ urls.py                      # /users/ endpoints (login, profile, recommendations)
│  └─ templates/                   # base.html, index, login, profile, recommendations
├─ db.sqlite3                      # Sample dev database
├─ manage.py
└─ requirements.txt
```

---

## Data Model

* **Movie**

  * `movie_id` (text, indexed) — external ID/key for the movie
  * `movie_name` (text, indexed)
  * `year` (int, indexed)
  * `certificate` (text) — e.g., G/PG/PG‑13/R/NC‑17
  * `runtime` (int, minutes)
  * `rating` (float)
  * `votes` (int)
  * M2M: `genres` → **MovieGenre**
  * M2M: `directors` → **MovieDirector**
  * M2M: `stars` → **MovieStar**

* **MovieGenre**, **MovieDirector**, **MovieStar**

  * `name` (text, indexed)

* **UserProfile**

  * `user` (OneToOne → auth.User)
  * `priority_movies_recommendations_dictionary` (Text, optional metadata)

* **MovieWatch**

  * `movie` (FK → Movie)
  * `user_profile` (FK → UserProfile, `related_name="movie_watches"`)
  * `watched_at` (datetime)
  * `is_finished` (bool)
  * `rating` (int: **-1** Disliked / **0** Neutral / **1** Liked)

---

## Getting Started

### Prerequisites

* Python **3.10+**
* (Optional) `pipx` or `virtualenv`

### Installation

```bash
# 1) Go to the project folder
cd Algorithmics-Movies-Project-master

# 2) Create & activate a virtual environment
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Apply migrations (safe to run even if db.sqlite3 already exists)
python manage.py migrate
```

### Run the app

```bash
python manage.py runserver
```

Then open **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

### Create an admin user

```bash
python manage.py createsuperuser
```

Admin panel: **/admin/**

> The repository ships with a `db.sqlite3` for convenience. You can use it as‑is, or delete it and start fresh (run migrations and optionally load your own data).

---

## Key URLs

* **Home / About** — `/`
* **Admin** — `/admin/`
* **Movies**

  * Top‑rated: `/movies/top-rated/`
  * Search: `/movies/search/`
  * Detail: `/movies/movie/<movie_id>/`
  * Mark/Update watch entry: `/movies/movie/<movie_id>/watch/`
* **Users**

  * Login: `/users/login/`
  * Profile (watch history): `/users/profile/`
  * Recommendations: `/users/recommendations/`

> Some pages (profile/recommendations) require authentication.

---

## Searching & Sorting

The **MovieSearchForm** supports:

* `name` (contains)
* `year` (exact)
* `genre` (select a genre)
* `actor` (select a star)
* `director` (select a director)
* `certificates` (multi‑select among G/PG/PG‑13/R/NC‑17)

Additionally, the view accepts a `sort` query parameter. Common examples:

```
/movies/search/?name=matrix&sort=rating
/movies/search/?year=1999&genre=Action
```

(See the UI controls on the search page for the exact options available.)

---

## Recommendations

Recommendations are generated from your **watch history** (data in `MovieWatch`), leveraging co‑occurrence patterns and basic heuristics, and then filtered to avoid already‑watched titles. Categories surfaced include:

* **Highly recommended** (top picks based on your history)
* **Films you would like** (similarity heuristics)
* **Popular** (globally popular/high‑vote titles)
* **Kids** (kid‑friendly by certificate)
* **Recent** (newer releases, e.g., after 2016)

> You’ll see a handful of randomized picks per category every time you load the recommendations page.
