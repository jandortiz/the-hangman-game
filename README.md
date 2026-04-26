# Hangman Game 🎯

A full-stack web-based Hangman game designed to practice English vocabulary while reinforcing backend and frontend development skills.

---

## About the project

This project is a classic Hangman (word guessing) game built from scratch as a learning exercise. The game fetches random English words from external APIs and provides dictionary definitions as hints, turning each round into a vocabulary-building experience.

The primary goals are twofold: on the **learning side**, it helps players discover and memorize English words through gameplay — each round reveals a new word with its definition, reinforcing retention through active recall. On the **technical side**, it serves as a hands-on project to strengthen skills in Python backend development with FastAPI and frontend development with vanilla HTML, CSS, and JavaScript.

---

## How it works

1. The player presses **START GAME** on the welcome screen.
2. The backend fetches a random English word from an external API and retrieves its definition from a dictionary API.
3. The player sees the hidden word as blank spaces along with a hint (the word's definition).
4. Using the on-screen QWERTY keyboard (or their physical keyboard), the player guesses one letter at a time.
5. Correct guesses reveal the letter in the word. Wrong guesses add a body part to the hangman figure (up to 6 mistakes).
6. The game ends when the player guesses all letters (win) or runs out of attempts (loss). The full word is revealed either way.
7. The player can press **PLAY AGAIN** to start a new round with a different word.

---

## Features

- **Random word generation** with dictionary definitions as hints, powered by external APIs with a local fallback word list for reliability.
- **Expressive SVG hangman figure** that changes facial expressions based on mistakes: smiling (0–1 errors), worried (2–4 errors), and panicking (5–6 errors).
- **3D keyboard effect** with visual feedback — correct letters turn brown, incorrect letters turn red, and all keys have a satisfying press animation.
- **Dark and light themes** with a toggle button, automatic persistence via localStorage, and a notebook-grid background texture.
- **Responsive design** that adapts to different screen sizes, from mobile phones to tablets and desktops.
- **Three-screen flow**: start screen → game screen → result screen, with smooth transitions between them.
- **Social footer** with links to GitHub, LinkedIn, and email.

---

## Tech stack

### Backend

- **FastAPI** — modern async web framework that serves both the API endpoints and the static frontend files.

### Frontend

- **HTML5** — semantic structure for the three game screens.
- **CSS3** — custom properties (CSS variables) for theming, Flexbox for layout, and CSS transitions for animations.
- **Vanilla JavaScript** — DOM manipulation, Fetch API for backend communication, event delegation for the keyboard, and localStorage for theme persistence.

### External APIs

- **Random Word API** (`random-word-api.herokuapp.com`) — provides random English words with configurable length and difficulty.
- **Free Dictionary API** (`api.dictionaryapi.dev`) — provides definitions, parts of speech, and phonetics for English words.


---

## Project structure

```
hangman-game/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app initialization, lifespan, router and static mount
│   ├── config.py              # Environment variable loading (Settings class)
│   ├── dependencies.py        # Shared dependency injectors
│   ├── exceptions.py          # Custom exception classes
│   ├── data/
│   │   └── fallback_words.json  # Offline word list for API fallback
│   ├── routers/
│   │   ├── __init__.py
│   │   └── game.py            # API endpoints: /new, /guess, /status
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── game.py            # Pydantic models for request/response validation
│   └── services/
│       ├── __init__.py
│       ├── game_service.py    # Game state management (create, guess, status)
│       └── word_service.py    # External API client (word + definition fetching)
├── static/
│   ├── index.html             # Main HTML with three game screens
│   ├── css/
│   │   └── style.css          # Styles, themes, animations
│   ├── js/
│   │   └── app.js             # Game logic, DOM updates, API calls
│   └── assets/
├── tests/
│   ├── __init__.py
│   └── test_game.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── README.md
```

---

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/game/new` | Creates a new game. Returns game ID, masked word, hint, and attempts remaining. |
| `POST` | `/api/game/{game_id}/guess` | Submits a letter guess. Returns whether it was correct, updated word, and game status. |
| `GET` | `/api/game/{game_id}/status` | Returns the current state of a game (for reconnection scenarios). |

---

## Getting started

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (optional, for containerized deployment)

### Local development

```bash
# Clone the repository
git clone https://github.com/your-username/hangman-game.git
cd hangman-game

# Install dependencies
uv sync

# Create environment file
cp .env.example .env

# Run the development server
uv run uvicorn app.main:app --reload --reload-dir app --reload-dir static
```

Open `http://127.0.0.1:8000` in your browser.



---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WORD_API_URL` | `https://random-word-api.herokuapp.com` | Base URL for the random word API |
| `DICTIONARY_API_URL` | `https://api.dictionaryapi.dev/api/v2/entries/en` | Base URL for the dictionary API |
| `ENVIRONMENT` | `development` | Current environment (development/production) |

---

## What I learned

This project reinforced several key concepts across the full stack:

**Backend (Python/FastAPI):** project structure with separation of concerns (routers, schemas, services), async programming with `async/await` for non-blocking API calls, dependency injection patterns, Pydantic validation, and environment-based configuration.

**Frontend (HTML/CSS/JS):** the box model and Flexbox layout, CSS custom properties for theming, DOM manipulation and event delegation, the Fetch API for backend communication, SVG rendering with dynamic content, and responsive design principles.

**DevOps:** Docker containerization with multi-stage builds, environment variable management, and cloud deployment with automatic CI/CD via GitHub integration.

---

## Author

**Jefferson Ortiz** — [@jandortiz](https://github.com/jandortiz)

---

## License

This project is open source and available under the [MIT License](LICENSE).