# Golf

A simple CodeGolf frontend.

### Features Implemented

- A user registration and authentication system
- Character count for submitted solutions
- User profile pages
- User profile modification forms
- Time based problems
- A ranking system

### TODO

- Achievements, badges for players

#### How to run a local instance?

 * Install: `python`, `postgresql`
 * Clone the repo.
 * Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
   and do `pip install -r requirements.txt`.
 * Configure `postgresql` on your machine and create a new database for this
   project.
 * Copy `golf/local_settings_example.py` to `golf/local_settings.py`, and
   modify the database settings.
 * `cd` to the cloned repo (while you're still in virtualenv) and run: `python manage.py collectstatic`, `python manage.py makemigrations users contests`, `python manage.py migrate`
 * Start the development server: `python manage.py runserver`.
 * Let me know if you're unable to run it on your machine.
