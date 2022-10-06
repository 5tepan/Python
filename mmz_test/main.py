from sqlalchemy import create_engine, VARCHAR, Integer, Table, Column, MetaData, VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import Flask, render_template

app = Flask(__name__) 


meta = MetaData()

engine = create_engine('mssql+pyodbc://LAPTOP-JOCVFETG/Library?driver=ODBC+Driver+17+for+SQL+Server')

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Country(Base):
    __tablename__ = 'country'
    id_country = Column(Integer, primary_key=True)
    country_name = Column(VARCHAR(50))

#m = session.query(Country.id_country, Country.country_name).all()
#print((m))


a = 1
if a == 1:
    @app.route('/app', methods=['GET', 'POST'])
    def SellCountry():
        m = session.query( Country.id_country,Country.country_name).all()
       
        return render_template('app.html', items=m)


    if __name__ == '__main__':  
        app.debug = True  
        app.run(port=5000)