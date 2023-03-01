<h1 align="center">Eco Genius</h1>
<p>"Eco Genius" is a web-based tool for learning and practicing life table theory, designed to complement the understanding and application of life table theory.</p>
<p>
    Follow the step-by-step instructions below to install all the necessary tools required to run the system on your machine. Read carefully to understand how the system is designed and the technologies used in its development.
</p>
<h2>Installation of Eco Genius</h2>
<ol>
    <li>Ensure 
        <a href="https://www.python.org/downloads/release/python-3710/">Python 3.7.10</a>
        is installed. You can download it from the official Python website: 
        <a href="https://www.python.org/downloads/release/python-3710/">
            https://www.python.org/downloads/release/python-3710/
        </a>
</li>
    <li>Clone the repository by executing the following command:</li>
    <pre><code>git clone https://github.com/ifnmgsal-inf/eco-genius.git
</code></pre>
    <li>Navigate to the project directory:</li>
    <pre><code>cd eco-genius
</code></pre>
    <li>Create a new file named `.env` in the root of the project.</li>
    <li>Open the `.env` file and fill in the following information:</li>
    <pre><code>NAME_DB = 'your_database_name'
USER_DB = 'your_database_username'
PASSWORD_DB = 'your_database_password'
HOST_DB = 'your_database_host'
PORT_DB = 'your_database_port'

EMAIL_HOST = 'your_smtp_server'
EMAIL_PORT = your_smtp_port
EMAIL_USE_TLS = True (or False)
EMAIL_HOST_USER = 'your_smtp_username'
EMAIL_HOST_PASSWORD = 'your_smtp_password'
DEFAULT_FROM_EMAIL = 'your_email@example.com'
</code></pre>
    <li>Save the `.env` file after making the necessary changes.</li>
    <li>Install the required packages:</li>
    <pre><code>pip install -r requirements.txt
</code></pre>
    <li>Configure the database:</li>
    <pre><code>python manage.py makemigrations
python manage.py migrate
</code></pre>
    <li>Create a superuser account:</li>
    <pre><code>python manage.py createsuperuser
</code></pre>
    <li>Run the development server:</li>
    <pre><code>python manage.py runserver 8000
</code></pre>
</ol>
<h2 align="center">Access</h2>
<p align="center">Now that everything is installed and configured, click the link below or enter the URL in your browser</p>
<p align="center"><b><a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a></b></p>
