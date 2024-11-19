import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pytest
from app import create_app, db
from app.models import Users

@pytest.fixture(scope='module')
def app():
    app = create_app(config_class='app.config.TestingConfig')
    with app.app_context():
        db.create_all()

        yield app
        db.session.remove()
        db.drop_all()
    
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Criar um usuário no banco"""
    user_existing = Users.query.filter_by(email = 'teste@test.com').first()

    if not user_existing:
        client.post('/users', json={
            'username': 'testuser',
            'password': 'testpassword',
            'name': 'teste',
            'email': 'teste@test.com',
            'author' : True
        })

    # Fazer login e capturar o token
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    token = response.json['token']  # Ajuste conforme sua aplicação
    return {'Authorization': f'Bearer {token}'}
