import tempfile
import pytest
from app import app as ppp
from api.instances.database import database
import os


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope='session')
def app():
    # server.set_config()
    app = ppp
    db = database.db

    db_fd, db_path = tempfile.mkstemp()
    
    app.config['DATABASE'] = db_path
    app.config['DEBUG'] = True
    app.config['TESTING'] = True 
    db.init_app(app)
    
    with app.app_context():
        db.create_all() 
    
    yield app  
    
    os.close(db_fd)
    os.unlink(db_path)


