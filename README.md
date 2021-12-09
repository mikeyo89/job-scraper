## Welcome to the Job Scraper project!

This project will analyze Indeed's HTML and extrapolate summary data -- such as the number of results that seek a particular Framework or Programming Language.
### View a demo of the application <a href="https://www.michaelbonilla.dev/scraper/">here</a>.###

### Steps to Reproduce

1. Clone this repo using git or github desktop.
2. In a local or virtual environment, ensure to install pip or pip3.\
   This can be done by checking out the documentation on <a href="https://pip.pypa.io/en/stable/installing/">pip</a>.
3. Navigate to the project directory -- 2 folders (research_scripts and web_app) and various files will be located here.
4. Open a command shell -- such as bash, windows shell, or zsh -- and run the following command:\
    `pip3 install -r requirements.txt`

### All dependencies are now installed!

**From here, simply run the web-app by doing the following:**
1. Navigate into the web_app directory.
2. In a command shell, run the following command:
    `python manage.py runserver`
3. Navigate to <a href="localhost:8000">localhost:8000</a> on your favorite browser.
4. You're free to use the application as you wish!

**... or navigate to the research_scripts folder and run any of the following files to locally try the project:**
```
1. mvp.py
2. mvp2.py
3. poc.py
4. poc2.py
```

_**Note:** `mvp.py` `mvp2.py` make **real** `GET` requests to Indeed. If you would prefer not to do so, run `poc.py`, `poc2.py`, or visit the demo of this app <a href="https://www.michaelbonilla.dev/scraper/">here</a> instead._


**That is all, folks!**
