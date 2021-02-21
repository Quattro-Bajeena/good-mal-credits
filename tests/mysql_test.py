import sqlalchemy

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Adelinold001@localhost:3306/gms'

# Test if it works
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
print(engine.table_names())