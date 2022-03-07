import tempfile
import pytest
from app import app as ppp
from api.instances.database import database
import os

# https://zetcode.com/python/faker/
from faker import Faker
from api.models.rate import RateModel, TypeRate
from api.schemas.rate import RateSchema


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def app():
    # server.set_config()
    app = ppp
    db = database.db

    db_fd, db_path = tempfile.mkstemp()

    app.config["DATABASE"] = db_path
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def fake_rate():
    fake = Faker()
    words = [tr.value for tr in TypeRate]
    return {
        "title": fake.word(),
        "content": fake.text(),
        "rate_type": fake.word(words),
        "rate": fake.random_int(1, 5),
    }


@pytest.fixture()
def fake_multi_rate():
    fake = Faker()
    words = [tr.value for tr in TypeRate]
    lista = []
    for i in range(3):
        lista.append(
            {
                "title": fake.word(),
                "content": fake.text(),
                "rate_type": fake.word(words),
                "rate": fake.random_int(1, 5),
            }
        )
    return lista


@pytest.fixture()
def all_rate(request):
    schema = RateSchema(many=True)
    return schema.dump(RateModel.find_all())


@pytest.fixture()
def one_rate():
    schema = RateSchema()
    return schema.dump(RateModel.find_first())
