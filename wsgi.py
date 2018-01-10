#!/usr/bin/env python3

from potnanny.application import create_app, configure_database

app = create_app()
configure_database(app)

if __name__ == '__main__':
    app.run()
