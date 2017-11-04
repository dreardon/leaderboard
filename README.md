

# Leaderboard

This is meant to be a simple ranking application for a small project team.
It is built with [Python][0] using [Django][1].

## Installation

To set up a development environment quickly, first install Python. Then install and configure virtualenv.

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py makemigrations
    python manage.py migrate

Finally, after creating a Django super user, log in to the admin screen, add teams and ranking results

You can override settings.py by creating a local_settings.py in the same directory.

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
