# First time installation

    :::console
    $ ./venv.sh
    $ source .venv/bin/activate
    (venv) $ ./manage.py syncdb
    (venv) $ ./manage.py collectstatic
    (venv) $ ./manage.py compilemessages

# Update

    :::console
     $ ./venv.sh update
     $ source .venv/bin/activate
     (venv) $ ./manage.py syncdb
     (venv) $ ./manage.py collectstatic
     (venv) $ ./manage.py compilemessages
