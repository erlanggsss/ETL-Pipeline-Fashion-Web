# Initiate python environment
py -m venv .env

# Activate env
Powershell
.env\Scripts\Activate\ps.1

CMD
.env\Scripts\Activate\bat

# install libraries in the requirements.txt file
pip install -r requirements.txt

# Creating a database in PostgreSQL
CREATE USER [DB_USER] WITH ENCRYPTED PASSWORD '[DB_PASSWORD]';
CREATE DATABASE [DB_NAME];

# Grant database access to users
GRANT ALL ON DATABASE [DB_NAME] TO [DB_USER];
ALTER DATABASE [DB_NAME] OWNER TO [DB_USER];

# Run the script
python main.py

# Login to postgres database
psql --username [DB_USER] --dbname [DB_NAME]
SELECT * FROM [TABLE_NAME];

# Run unit test
python -m pytest tests

# Run coverage test
coverage run -m pytest tests

# Check coverage test results
coverage html

# Google Sheets URL:
https://docs.google.com/spreadsheets/d/1EUa65GLeKgyEoZMAnOvYIj4DdctIzn4f_MSKijFxVVQ/edit?usp=sharing
