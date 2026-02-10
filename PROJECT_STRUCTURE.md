# Project Structure

The project has been restructured into two main directories:

## `backend/`
Contains the Flask application code.
- **Run**: `cd backend` -> `python app.py` (or `flask run`)
- **Key Files**: 
    - `app.py`: Main entry point.
    - `models/`: Database models.
    - `routes/`: API endpoints.
    - `config.py`: Configuration settings.

## `frontend/`
Contains the React frontend application.
- **Run**: `cd frontend` -> `npm start`
- **Build**: `cd frontend` -> `npm run build`

## Root
- `venv/`: Python virtual environment (keep activating this as before).
- `README.md`: Project documentation.

## Running the App
1.  **Backend**: Open a terminal, `cd backend`, then run `python app.py`.
2.  **Frontend**: Open another terminal, `cd frontend`, then run `npm start`.
