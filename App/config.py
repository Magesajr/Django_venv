import os 
base=os.path.abspath(os.path.dirname(__file__))
database=os.path.join(base,'database')
Upload=os.path.join(base,'Uploads')

class Config:
    if not  os.path.exists(database):
        os.makedirs(database)
    if not  os.path.exists(Upload):
        os.makedirs(Upload)
    
    SECRET_KEY='testing'
    UPLOAD_FOLDER=Upload
    app_name='magesaapp'
    app_id='2ba67794-4571-450a-b041-beaa698bcc8c'
    CLID='2ba67794-4571-450a-b041-beaa698bcc8c'
    TOKEN='379e0795-987d-4d1b-8f8f-6cad8bb6cabb'
    client_secret='HfRyLG/N7taR3K1uzEo3qAnOqzAOd34wVXI/A7p5nHJefClIh/6HzBieGLXnLuJL28QI45ZhQ89VvIRslAMlSiuh2c2lMQtaZkmOq53YiftlNyi/7ERKmPZu4M0gDbcBgVf38waprNv2A56mj8O3E1ItlAMILFre0bv59LVds4oBG7YesQJR6yld2eiTTGuS5shOTa57Aqof2geKayEj1zcY9HJ0d3PgWgY6RmIPRLmbNHVoSMqaw9rV0//NTu82yaCDkUxQYhjc9bZH3tISXIk9MQKEFF5EEHCWm7E7GfFWW/jycN6S1m13RlesBq15VwaccRgYBFyO6S+UCfwS9FoMn8e+PbnwsxQ+EJKxwDIk6cnJg4i0lKRLZJDPX/okPdM1P6VmY37qgZ4B+92OcpaLL1P+EuIuzHURMT4E7ZAOHDW11Cwiw40isO0BBdg551wF5Ht+pGkSoF5jyZHFrCG0wi9nod+z7b+E3RjZuVVv61E27wCUJfJNeMXcJlglerJNUdm0z/NtkqDhMiWD8QaOjSFNBO8hoyzoNk8lhlyHKowazEEiayxucu0HZGr+nGZYx4PYs+vvbGIuKGJEyB792i+XGp34z6fTpnz0/Mzl0OuJp9nNuJiAlxkzWD18ttkHWR37Rl5GE9Xbr/9pzzkRO0WvfKpcI8TIxTGV0qo='

    
    @staticmethod
    def init_app(app):
        pass

class Development(Config):
    MAIL_SERVER='localhost'#'smtp.gmail.com'
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    #MAIL_USE_TLS=True
    MAIL_PORT=1025
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ database + '/data.sqlite'

class Testing(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ database + '/testing.sqlite'

    


class Production(Config):
    SQLALCHEMY_DATABASE_URI=''
    pass

config={
    'default':Development,
    'testing':Testing,
    'deploy':Production
}

