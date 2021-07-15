# discoball

Discord bot written with `discord.py` hosted on `Heroku` 

## Install
```
virtualenv venv
source venv/bin/activate    # Linux / OSX
venv/Scripts/activate.ps1   # Windows powershell
pip install -r requirements.txt
```

## Run locally
```
BOT_TOKEN=token python client.py
APP_ENV=production BOT_TOKEN=token python client.py     # set APP_ENV=production to sync commands
```

## Useful reading
<https://discord-py-slash-command.readthedocs.io/en/latest/>