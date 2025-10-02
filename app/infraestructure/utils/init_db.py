from app.infraestructure.utils.db import engine
from app.infraestructure.utils.tables import Base
from app.infraestructure.utils.models import User, Product, Sale

Base.metadata.create_all(bind=engine, checkfirst=True)
