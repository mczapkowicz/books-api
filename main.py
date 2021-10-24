from core.rate_limiter import limiter
from create_app import create_app

app = create_app()

limiter.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)