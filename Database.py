from config import host, user, password, port, db_name
import psycopg2
import random


class Database:

    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.connection.autocommit = True

    def create_DB(self):
        try:
            self.create_tables()
            self.first_insert_in_tables()
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if self.connection:
                self.connection.close()
            print("[INFO] PostgreSQL connection closed")

    def create_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE train(
                id serial PRIMARY KEY,
                type varchar(100) NOT NULL,
                model_locomotive int NOT NULL,
                number_of_wagons int NOT NULL);"""
            )
            cursor.execute(
                """CREATE TABLE station(
                id serial PRIMARY KEY,
                name varchar(100) NOT NULL,
                type varchar(100) NOT NULL);"""
            )

            cursor.execute(
                """CREATE TABLE direction_travel(
                id serial PRIMARY KEY,
                start_station int references station(id) ON DELETE CASCADE,
                finish_station int references station(id) ON DELETE CASCADE,
                number_branch int NOT NULL);"""
            )

            cursor.execute(
                """CREATE TABLE route(
                id serial PRIMARY KEY,
                direction_id int references direction_travel(id) ON DELETE CASCADE,
                start_time date NOT NULL,
                finish_time date NOT NULL,
                number_train int references train(id) ON DELETE CASCADE);"""
            )
            print("[INFO] Table created successfully")

    def first_insert_in_tables(self):
        with self.connection.cursor() as cursor:
            type_t = ['пассажирский', 'грузовой', 'скоростной']
            model = 3000
            num = 1
            for i in range(10):
                model += 1
                num = random.randint(2, 25)
                type_train = random.choice(type_t)
                cursor.execute(
                    f"""INSERT INTO train (type, model_locomotive, number_of_wagons) VALUES
                    ('{type_train}', {model}, {num});"""
                )

            type_st = ['грузовая', 'пассажирская']
            name_st = ['Воронеж', 'Москва', 'Орёл', 'Тамбов', 'Екатеринбург']
            for i in range(5):
                type_st1 = random.choice(type_st)
                random_int = random.randint(1, 10)
                name_st1 = name_st[i] + f'_{random_int}'
                cursor.execute(
                    f"""INSERT INTO station (name, type) VALUES
                    ('{name_st1}', '{type_st1}');"""
                )

            for i in range(5):
                cursor.execute(
                    f"""INSERT INTO direction_travel (start_station, finish_station, number_branch) VALUES
                    ({random.randint(1, 5)}, {random.randint(1, 5)}, {random.randint(1, 10)});"""
                )

            start_date = ['2002-10-12', '2003-09-17', '2006-12-13', '2001-06-05', '2007-04-28']
            finish_date = ['2002-10-20', '2003-09-27', '2006-12-21', '2001-06-13', '2007-05-09']
            for i in range(5):
                cursor.execute(
                    f"""INSERT INTO route (direction_id, start_time, finish_time, number_train) VALUES
                    ({random.randint(1, 5)}, '{start_date[i]}', '{finish_date[i]}', {random.randint(1, 10)});"""
                )

            print("[INFO] Data was successfully inserted")

    def drop_tables(self):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    """DROP TABLE route;"""
                )
                cursor.execute(
                    """DROP TABLE direction_travel;"""
                )
                cursor.execute(
                    """DROP TABLE train;"""
                )
                cursor.execute(
                    """DROP TABLE station;"""
                )
                print("[INFO] Table was deleted")
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if self.connection:
                    self.connection.close()
                    print("[INFO] PostgreSQL connection closed")

    def select_all(self, table):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"""SELECT * FROM {table};"""
                )
                print("[INFO] Select is good")
                return cursor.fetchall()
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)

    def delete_line(self, id, table):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"""DELETE FROM {table} WHERE id = {id};"""
                )
                print("[INFO] Delete is good")
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)

    def insert_route(self, num_dir, start, finish, num_train):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"""INSERT INTO route (direction_id, start_time, finish_time, number_train) VALUES
                    ({num_dir}, '{start}', '{finish}', {num_train});"""
                )
                print("[INFO] Insert is good")
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)

    def insert_station(self, name, type):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"""INSERT INTO station (name, type) VALUES
                    ('{name}', '{type}');"""
                )
                print("[INFO] Insert is good")
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)

    def insert_direction(self, start, finish, num_branch):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"""INSERT INTO direction_travel (start_station, finish_station, number_branch) VALUES
                       ('{start}', '{finish}', '{num_branch}');"""
                )
                print("[INFO] Insert is good")
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)