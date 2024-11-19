from app import create_app
from dotenv import load_dotenv
from app import config 




load_dotenv()
app = create_app(config_class=config.Config)


if __name__ == '__main__':
    app.run(debug=True)