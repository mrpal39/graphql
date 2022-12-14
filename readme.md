###source venv/local/bin/activate
        sudo lsof -t -i tcp:8000 | xargs kill -9
