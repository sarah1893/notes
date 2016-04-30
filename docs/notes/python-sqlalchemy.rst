Python SQLAlchemy Chatsheet
=============================

Sqlalchemy Support DBAPI - PEP249
-----------------------------------

.. code-block:: python

    from sqlalchemy import create_engine 

    db_uri = "sqlite:///db.sqlite"
    engine = create_engine(db_uri)

    # DBAPI - PEP249
    # create table
    engine.execute('CREATE TABLE "EX1" ('
                   'id INTEGER NOT NULL,' 
                   'name VARCHAR, '
                   'PRIMARY KEY (id)'
                   ');')
    # insert a raw
    engine.execute('INSERT INTO "EX1" '
                   '(id, name) '
                   'VALUES (1,"raw1")')

    # select *
    result = engine.execute('SELECT * FROM '
                            '"EX1"')
    for _r in result:
       print _r

    # delete *
    engine.execute('DELETE from "EX1"'
                   'where id=1;')
    result = engine.execute('SELECT * FROM '
                            '"EX1"')
    print result.fetchall()


Transaction and Connect Object
--------------------------------

.. code-block:: python

    from sqlalchemy import create_engine

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    # Create connection
    conn = engine.connect()
    # Begin transaction
    trans = conn.begin()
    conn.execute('INSERT INTO "EX1" (name) '
                 'VALUES ("Hello")')
    trans.commit()
    # Close connection
    conn.close()


Metadata - Generating Database Schema
--------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer, String

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    # Create a metadata instance
    metadata = MetaData(engine)
    # Declare a table
    table = Table('Example',metadata,
                  Column('id',Integer, primary_key=True),
                  Column('name',String))
    # Create all tables
    metadata.create_all()
    for _t in metadata.tables:
       print "Table: ", _t

Inspect - Get Database Information
------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import inspect

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    inspector = inspect(engine)

    # Get table information
    print inspector.get_table_names()

    # Get column information
    print inspector.get_columns('EX1')


Reflection - Loading Table from Existing Database
---------------------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table 

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    # Create a MetaData instance
    metadata = MetaData()
    print metadata.tables

    # reflect db schema to MetaData
    metadata.reflect(bind=engine)
    print metadata.tables

Get Table from MetaData
------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    # Create MetaData instance
    metadata = MetaData(engine, reflect=True)
    print metadata.tables

    # Get Table
    ex_table = metadata.tables['Example'] 
    print ex_table


Create all Tables Store in "MetaData"
--------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer, String

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)
    meta = MetaData(engine)

    # Register t1, t2 to metadata
    t1 = Table('EX1', meta,
               Column('id',Integer,
                       primary_key=True),
               Column('name',String))

    t2 = Table('EX2', meta,
               Column('id',Integer,
                       primary_key=True),
               Column('val',Integer))
    # Create all tables in meta
    meta.create_all()

Create Specific Table
-----------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer, String

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    meta = MetaData(engine)
    t1 = Table('Table_1', meta,
               Column('id', Integer, primary_key=True),
               Column('name',String))
    t2 = Table('Table_2', meta,
               Column('id', Integer, primary_key=True),
               Column('val',Integer))
    t1.create()

Some Table Object Operation
----------------------------

.. code-block:: python

    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer, String

    meta = MetaData()
    t = Table('ex_table', meta,
              Column('id', Integer,
                     primary_key=True),
              Column('key', String),
              Column('val', Integer))
    # Get Table Name
    print t.name

    # Get Columns
    print t.columns.keys()

    # Get Column
    c = t.c.key
    print c.name
    # Or
    c = t.columns.key
    print c.name

    # Get Table from Column
    print c.table


SQL Expression Language
-------------------------

.. code-block:: python

    # Think Column as "ColumnElement"
    # Implement via overwrite special function
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer, String
    from sqlalchemy import or_

    meta = MetaData()
    table = Table('example', meta,
                  Column('id', Integer,
                     primary_key=True),
                  Column('l_name', String),
                  Column('f_name', String))
    # sql expression binary object 
    print repr(table.c.l_name == 'ed')
    # exhbit sql expression
    print str(table.c.l_name == 'ed')

    print repr(table.c.f_name != 'ed')

    # comparsion operator
    print repr(table.c.id > 3)

    # or expression
    print (table.c.id > 5) | (table.c.id < 2)
    # Equal to
    print or_(table.c.id > 5, table.c.id < 2)

    # compare to None produce IS NULL 
    print (table.c.l_name == None)
    # Equal to
    print (table.c.l_name.is_(None))

    # + means "addition"
    print (table.c.id + 5)
    # or means "string concatenation"
    print (table.c.l_name + "some name")

    # in expression
    print (table.c.l_name.in_(['a','b']))

insert() - Create an "INSERT" Statement
----------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer
    from sqlalchemy import String

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    # create table
    meta = MetaData(engine)
    table = Table('user', meta, 
       Column('id', Integer, primary_key=True),
       Column('l_name', String),
       Column('f_name', String))
    meta.create_all()

    # insert data via insert() construct
    ins = table.insert().values(
          l_name='Hello',
          f_name='World')
    conn = engine.connect()
    conn.execute(ins)

    # insert multiple data
    conn.execute(table.insert(),[
       {'l_name':'Hi','f_name':'bob'},
       {'l_name':'yo','f_name':'alice'}])


select() - Create a "SELECT" Statement
---------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import select
    from sqlalchemy import or_

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)
    conn = engine.connect()

    meta = MetaData(engine,reflect=True)
    table = meta.tables['user']

    # select * from 'user'
    select_st = select([table]).where(
       table.c.l_name == 'Hello') 
    res = conn.execute(select_st) 
    for _row in res: print _row

    # or equal to
    select_st = table.select().where(
       table.c.l_name == 'Hello')
    res = conn.execute(select_st) 
    for _row in res: print _row

    # combine with "OR"
    select_st = select([
       table.c.l_name, 
       table.c.f_name]).where(or_(
          table.c.l_name == 'Hello',
          table.c.l_name == 'Hi'))
    res = conn.execute(select_st)
    for _row in res: print _row

    # combine with "ORDER_BY"
    select_st = select([table]).where(or_(
          table.c.l_name == 'Hello',
          table.c.l_name == 'Hi')).order_by(table.c.f_name)
    res = conn.execute(select_st)
    for _row in res: print _row

join() - Joined Two Tables via "JOIN" Statement
------------------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer
    from sqlalchemy import String
    from sqlalchemy import select

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    meta = MetaData(engine, reflect=True)
    email_t = Table('email_addr', meta,
          Column('id', Integer, primary_key=True),
          Column('email',String),
          Column('name',String))
    meta.create_all()

    # get user table
    user_t = meta.tables['user']

    # insert
    conn = engine.connect()
    conn.execute(email_t.insert(),[
       {'email':'ker@test','name':'Hi'},
       {'email':'yo@test','name':'Hello'}])
    # join statement
    join_obj = user_t.join(email_t,
       email_t.c.name == user_t.c.l_name)
    # using select_from
    sel_st = select(
       [user_t.c.l_name, email_t.c.email]).select_from(join_obj)
    res = conn.execute(sel_st)
    for _row in res: print _row

Delete Rows from Table
------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)
    conn = engine.connect()

    meta = MetaData(engine, reflect=True)
    user_t = meta.tables['user']

    # select * from user_t
    sel_st = user_t.select()
    res = conn.execute(sel_st)
    for _row in res: print _row

    # delete l_name == 'Hello'
    del_st = user_t.delete().where(
          user_t.c.l_name == 'Hello')
    print '----- delete -----'
    res = conn.execute(del_st)

    # check rows has been delete
    sel_st = user_t.select()
    res = conn.execute(sel_st)
    for _row in res: print _row

Check Table Existing
----------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Column
    from sqlalchemy import Integer, String
    from sqlalchemy import inspect
    from sqlalchemy.ext.declarative import declarative_base

    Modal = declarative_base()
    class Example(Modal):
       __tablename__ = "ex_t"
       id = Column(Integer, primary_key=True)
       name = Column(String(20))

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)
    Modal.metadata.create_all(engine)

    # check register table exist to Modal
    for _t in Modal.metadata.tables:
       print _t

    # check all table in database
    meta = MetaData(engine, reflect=True)
    for _t in meta.tables:
       print _t

    # check table names exists via inspect
    ins = inspect(engine)
    for _t in ins.get_table_names():
       print _t


