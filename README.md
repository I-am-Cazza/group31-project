Ensure you have Python version 3.7.* installed (Ideally 3.7.2)

1. Run `git clone https://github.com/I-am-Cazza/group31-project.git` to clone a local copy of the repository.
2. (Optional) Create a python virtual environment to install the required packages. This isn’t required but is strongly recommended as it avoids potential conflicts with your existing python packages. To create a virtual environment.
	1. `sudo -H pip3 install virtualenv` (unfortunately can’t do this on DCS machines but they might already have virtualenv?)
	2. Navigate to the project root.
	3. `virtualenv venv`
	4. `source venv/bin/activate`
	5. You’ll now be working using the virtual environment. You’ll need to run `source venv/bin/activate` for each terminal session when you want to work on the project.
	6. If at any time you want to deactivate the virtual environment and go back to normal python, run `deactivate`.
3. Run `pip install -r requirements.txt` from the project root to install the dependencies. **If you aren’t using a virtual environment, you’ll probably need to use `pip3` instead of `pip`.**
4. Install a PostGreSQL database with the settings configured as such: Name: cs261project, User: cs261, Password: cs261abcgrr
5. Run `python manage.py makemigrations` followed by `python manage.py migrate` (again, substitute `python` for `python3` if you aren’t using a virtual environment). This will create the database schema and apply it to the database.
6. Run `python manage.py runserver 8000`. Go to https://127.0.0.1:8000/ and view the web app.

