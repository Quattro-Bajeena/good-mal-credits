import sqlalchemy

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://gms_app:Adelinold001@paraon.xyz:3306/gms'

# Test if it works
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
print(engine.table_names())