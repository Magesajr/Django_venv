import unittest
from App import create_app,db
from App.models import Ticket
from flask import current_app

class BasicTestcase(unittest.TestCase):
    def setUp(self):
        self.app =create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertTrue(current_app is not None)
    
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


class TicketTestcase(unittest.TestCase):
    def test_user_registration(self):
        user=Ticket(name='mimi',email='mimi@example.com',
                    start_point='Kigoma',destination='Dar',phonenumber='09008467696')
        db.session.add(user)
        db.session.commit()

    def test_user_registrations_delete(self):
        mimi=Ticket.query.filter_by(name='mimi').first()
        db.session.delete(mimi)
        db.session.commit()
