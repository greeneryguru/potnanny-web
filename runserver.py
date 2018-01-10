#!/usr/bin/env python3

import argparse
from potnanny.application import create_app, configure_database
from potnanny.config import DebugConfig

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask App')
    parser.add_argument('--debug', action='store_true', 
                        help='run werkzeug server in debug config mode')
    args = parser.parse_args()

    if args.debug:
        app = create_app(config=DebugConfig)
    else:
        app = create_app()
    
    configure_database(app)  
    app.run()