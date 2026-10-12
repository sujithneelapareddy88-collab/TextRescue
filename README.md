# TextRescue – Important Message and Deadline Detector

## Features
- Paste announcements and messages for analysis
- Extract likely tasks, dates, events, and deadlines
- Rule-based High / Medium / Low priority classification
- Review extracted results before saving
- SQLite persistence for saved tasks
- Mark tasks as Pending or Completed, delete tasks, and export CSV

## Run on macOS (VS Code)
1. Open this folder in VS Code.
2. Open Terminal in VS Code.
3. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL printed in the terminal (usually http://localhost:8501).

## Important
- The database file `textrescue.db` is created automatically beside `app.py`.
- Check extracted dates and priorities before relying on them.
- This is a prototype using keyword rules and date parsing, not a trained machine-learning model.
