from conf import Session
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from conf import engine

Base = declarative_base()


class Dad(Base):
    __tablename__ = 'dads'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    # my_sons = relationship("Son", back_ref='my_dad')
    my_sons = relationship("Son", back_populates='my_dad')


association_table = Table('association', Base.metadata,
    Column('son_id', Integer, ForeignKey('sons.id')),
    Column('toy_id', Integer, ForeignKey('toys.id'))
)


class Son(Base):
    __tablename__ = 'sons'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    dad_id = Column(Integer, ForeignKey('dads.id'))

    my_dad = relationship("Dad", back_populates='my_sons')
    my_toys = relationship('Toy', secondary=association_table, back_populates='my_owners')

class Toy(Base):
    __tablename__ = 'toys'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    my_owners = relationship('Son', secondary=association_table, back_populates='my_toys')
    


if __name__ == '__main__':
    try:
        ses = Session()
        ses.execute("SELECT 1;")

        association_table.drop(engine)
        Toy.__table__.drop(engine)
        Son.__table__.drop(engine)
        Dad.__table__.drop(engine)

        Base.metadata.create_all(engine)
        dad = Dad(name='Robert')
        
        # Hard Way 
        #ses.add(dad)

        #ses.commit()

        #son  = Son(id=1, name='Adas', dad_id=1)
        #ses.add(son)

        #son  = Son(id=2, name='Jasio', dad_id=1)
        #ses.add(son)

        #son  = Son(id=3, name='Stasio', dad_id=1)
        #ses.add(son)
        #...

        # we don't worry about id and foregin keys
        bike = Toy(name='bike')
        ball = Toy(name='ball')
        book = Toy(name='book')

        son1 = Son(name='Adas')
        son1.my_toys.append(ball)
        son1.my_toys.append(bike)

        son2 = Son(name='Jasio')
        son2.my_toys.append(ball)

        son3 = Son(name='Stasio')
        son3.my_toys.append(ball)
        son3.my_toys.append(bike)
        son3.my_toys.append(book)

        dad.my_sons.append(son1)
        dad.my_sons.append(son2)
        dad.my_sons.append(son3)
        
        ses.add(dad)

        ses.commit()

        print("Built and inserted")
    except Exception as e:
        print(e)
        raise(e)