# aviant-case-2024
Case solution for Aviant summer internship 2024.

# How to run
1. Clone the repository, cd into it
    * (Optional) Create a virtual environment, e.g.:
        - `python -m venv venv`
        - `source venv/bin/activate`
2. Install the requirements:
    * `pip install -r requirements.txt`
3. cd into `restaurant`-folder, run the following commands:
    * `python generate_init.py`
        - Runs Django migrations automatically
        - Creates dummy data for the database
        - ! Might overwrite existing data in the database !
    * `python manage.py runserver`
        - This will start the Django server
    * `python manage.py tailwind start`
        - This will start the TailwindCSS compiler (if working in developer mode, without static CSS files)
4. Go to `localhost:8000` or `127.0.0.1:8000` to see the website
