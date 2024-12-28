from flask import current_app
from App import db,create_app
from flask_migrate import Migrate
from App.models import Ticket,Routes


app=create_app('default')
migrate=Migrate(app,db)

@app.shell_context_processor
def make_shell():
    return dict(
        db=db,
        tick=Ticket(),
        route=Routes()
    )

@app.cli.command()
def test():
    '''Running Test..
Online Tickets Tests...'''
    import unittest
    tests=unittest.TestLoader().discover('App/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ =='__main__':
    app.run(debug=True)

