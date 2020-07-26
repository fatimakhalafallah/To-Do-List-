from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

def __repr__(self):
    return self.task

#creation of Database
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


menu=["1) Today's tasks",
      "2) Week's tasks","3) All tasks",
      "4) Missed tasks", "5) Add task",
      "6) Delete task", "0) Exit"]

while True:
    for i in menu:
        print(i)
    menuinput = input()
    if menuinput == '0':
        print('Bye!')
        break
    elif menuinput == '1':
        dy=datetime.today().day
        mn=datetime.today().strftime('%b')
        print(f'Today {dy} {mn}:')
        today = datetime.today().date()
        rows = session.query(Table).filter(Table.deadline == today).all()
        if rows == []:
            print('Nothing to do!')
        elif rows is not None:
            for rw in rows:
                print(rw.task)
    elif menuinput == '2':
        for i in range(0, 8):
            x = datetime.now() + timedelta(days=i)
            z = x.date()
            mn = z.strftime('%b')
            dy = z.strftime('%d')
            daay = z.strftime('%A')
            # Sunday 26 Apr:
            print('')
            print(f'{daay} {dy} {mn}:')
            rows = session.query(Table).filter(Table.deadline == z).all()
            if rows == []:
                print('Nothing to do!')
            elif rows is not None:
                for rw in rows:
                    print(rw.task)
            print(' ')
    elif menuinput == '3':
        print('All tasks:')
        # rows = session.query(Table).order_by(Table.deadline.asc()).all()
        rows = session.query(Table).order_by(Table.deadline).all()
        num = 0
        for rw in rows:
            x = rw.deadline
            mn = x.strftime('%b')
            dy = x.strftime('%d').lstrip("0").replace(" 0", " ")
            num += 1
            # 1.Meet my friends.28 Apr
            print(f'{num}. {rw.task}. {dy} {mn}')
    elif menuinput == '4':
            todate = datetime.today().date()
            rows = session.query(Table).order_by(Table.deadline < todate).all()
            print('Missed tasks:')
            num = 0
            if rows == []:
                print('Nothing is missed!')
            else:
                for row in rows:
                    if todate > row.deadline:
                        num += 1
                        x = row.deadline
                        mn = x.strftime('%b')
                        dy = x.strftime('%d').lstrip("0").replace(" 0", " ")
                        print(f'{num}. {row.task}. {dy} {mn}')
            print('')

    elif menuinput == '5':
        print('Enter Task')
        Entertask = input()
        print('Enter deadline')
        #YYYY-MM-DD.
        EnterDealine = input()
        datetime_object = datetime.strptime(EnterDealine, '%Y-%m-%d')
        new_row = Table(task=Entertask,deadline=datetime_object)
        session.add(new_row)
        session.commit()
        print('The task has been added!')
    elif menuinput == '6':
        print('Chose the number of the task you want to delete:')
        rows = session.query(Table).order_by(Table.deadline.asc()).all()
        nums = 0
        dic = {}
        if rows == []:
            print('Nothing to delete')
        else:
            for row in rows:
                x = row.deadline
                mn = x.strftime('%b')
                dy = x.strftime('%d').lstrip("0").replace(" 0", " ")
                nums += 1
                dic[nums] = row.id
                print(f'{nums}. {row.task}. {dy} {mn}')
        rowde = int(input())
        delrow = dic[rowde]
        x = session.query(Table).get(delrow)
        session.delete(x)
        session.commit()
        print('The task has been deleted!')


