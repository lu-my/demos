from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
migrate = Migrate()
photos = UploadSet('PHOTO', IMAGES)
cache = Cache(config={
    "CACHE_TYPE": "redis"
})


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    configure_uploads(app, photos)
    cache.init_app(app)
