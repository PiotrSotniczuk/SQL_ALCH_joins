from conf import Session
from build import Dad, Son, Toy
from sqlalchemy import join, select


try:
    ses = Session()


    # ------ EXECUTE ------- #
    print("Execute")
    j = Dad.__table__.join(Son)
    s = select([Dad, Son]).select_from(j)
    print(s)

    res = ses.execute(s)
    for row in res:
        # nie wygodny format
        print(row)

    





    # ------ QUERY ------- #

    # Brutall
    print("\nBrutal joins")
    res = ses.query(Dad, Son).filter(Dad.id == Son.dad_id).all()
    for d, s in res:
        print(d.name, s.name)



    # Lepiej
    print("\nFrom relationship")
    res = ses.query(Dad).all()
    for d in res:
        for s in d.my_sons:
            print(d.name,s.name, s.my_toys)





except Exception as e:
    print(e)
    raise(e)