#!/usr/bin/env python3


"""

check latest db measurements and see if actions need to be taken.

"""

import os
import sys
import re
import time
import datetime
sys.path.append( os.environ.get('FLASK_APP','/var/www/potnanny') )
from potnanny.application import create_app
from potnanny.extensions import db
from potnanny.apps.action.models import Action, ActionProcess
from potnanny.apps.outlet.models import Outlet
from potnanny.apps.measurement.models import MeasurementType, Measurement
from potnanny.apps.admin.models import Setting
from potnanny.lib.messenger import Messenger


# globals
pause_seconds = 30


def main():
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    poll = Setting.query.filter(Setting.name == 'polling interval minutes').first()
    if not poll:
        # logger.error("could not determine polling interval from db")
        sys.stderr.write("error. could not determine polling interval from db\n")
        sys.exit(1)

    if now.minute % poll.value:
        # now is not the right time to be running this
        sys.exit(0)
    else:
        then = now - datetime.timedelta(minutes=poll.value)
        actions = actions = Action.query.filter(
            Action.enabled == True
        ).all()
        if not actions:
            sys.exit(0)

        # sleep?
        # yes, pause to let any polling jobs finish collecting new 
        # measurements, before we begin evaluating them
        time.sleep(pause_seconds)
        mgr = ActionManager()
        for a in actions:
            mgr.init_action(a, then, now)

        sys.exit(0)

if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    main()

