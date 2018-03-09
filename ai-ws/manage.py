# manage.py
# this initializes the flask app to prepare the api configuration and logging

import unittest


from flask_script import Manager

from ai import create_app

import logging
log = logging.getLogger(__name__)

log.setLevel(logging.ERROR)

app = create_app()
manager = Manager(app)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('ot_ws/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()