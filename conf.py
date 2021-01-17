from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://ps:ps@localhost:5432/sqlalchjoin')

Session = sessionmaker(bind=engine)