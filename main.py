from Database import Database
from flask import Flask, render_template, url_for, request, flash

db = Database()
# db.drop_tables()
# db.create_DB()

menu = [{"name": "Информация о сайте", "url": "/"},
        {"name": "Маршруты", "url": "route"},
        {"name": "Станции", "url": "station"},
        {"name": "Направления следования", "url": "direction"},
        {"name": "Обратная связь", "url": "contact"}]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shf1vb2oa4shv327hd308y4'


@app.route("/")
def index():
    return render_template('index.html', title='О сайте', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title='О сайте')


def search_start(start_station):
    routes = db.select_all('route')
    directions = db.select_all('direction_travel')
    stations = db.select_all('station')
    new_routes = []
    for one_route in routes:
        for one_dir in directions:
            if one_route[1] == one_dir[0]:
                for one_stat in stations:
                    if one_dir[1] == one_stat[0]:
                        if one_stat[1] == start_station:
                            new_routes.append(one_route)
    return new_routes


def search_finish(finish_station):
    routes = db.select_all('route')
    directions = db.select_all('direction_travel')
    stations = db.select_all('station')
    new_routes = []
    for one_route in routes:
        for one_dir in directions:
            if one_route[1] == one_dir[0]:
                for one_stat in stations:
                    if one_dir[2] == one_stat[0]:
                        if one_stat[1] == finish_station:
                            new_routes.append(one_route)
    return new_routes


@app.route("/route", methods=["GET", "POST"])
def route():
    directions = db.select_all('direction_travel')
    routes = db.select_all('route')
    stations = db.select_all('station')
    if request.method == 'POST':
        if request.form['button'] == 'Удалить':
            db.delete_line(request.form['num_dir'], 'route')

            directions = db.select_all('direction_travel')
            routes = db.select_all('route')
            stations = db.select_all('station')
        if request.form['button'] == 'Добавить':
            db.insert_route(request.form['num_direction'], request.form['start_time'], request.form['finish_time'],
                            request.form['num_train'])

            directions = db.select_all('direction_travel')
            routes = db.select_all('route')
            stations = db.select_all('station')
        if request.form['button'] == 'Поиск_отбытие':
            directions = db.select_all('direction_travel')
            routes = search_start(request.form['search_start'])
            stations = db.select_all('station')
        if request.form['button'] == 'Поиск_прибытие':
            directions = db.select_all('direction_travel')
            routes = search_finish(request.form['search_finish'])
            stations = db.select_all('station')

    all_dir = []
    for i in range(len(routes)):
        dir = {}

        dir['number'] = routes[i][0]
        id_dir = routes[i][1]
        id_st1 = 0
        for z in range(len(directions) + 1):
            if z == id_dir:
                id_st1 = directions[z - 1][1]
        for j in range(len(stations) + 1):
            if j == id_st1:
                dir['start'] = stations[id_st1 - 1][1]  # станция отбытия

        id_dir = routes[i][1]
        id_st2 = 0
        for z in range(len(directions) + 1):
            if z == id_dir:
                id_st2 = directions[z - 1][2]
        for j in range(len(stations) + 1):
            if j == id_st2:
                dir['finish'] = stations[id_st2 - 1][1]  # станция прибытия

        dir['start_time'] = routes[i][2]  # время отбытия
        dir['finish_time'] = routes[i][3]  # время прибытия
        dir['train'] = routes[i][4]  # номер поезда

        all_dir.append(dir)

    return render_template('route.html', title='Маршруты', menu=menu, all_dir=all_dir, num_route=len(routes))


@app.route("/station", methods=["GET", "POST"])
def station():
    if request.method == 'POST':
        if request.form['button'] == 'Удалить':
            db.delete_line(request.form['num_stat'], 'station')
        if request.form['button'] == 'Добавить':
            db.insert_station(request.form['name'], request.form['type'])

    stations = db.select_all('station')

    all_stations = []
    for i in range(len(stations)):
        stat = {"id": stations[i][0], "name": stations[i][1], "type": stations[i][2]}
        all_stations.append(stat)
    return render_template('station.html', title='Станции', menu=menu, stations=all_stations, num_station=len(stations))


@app.route("/direction", methods=["GET", "POST"])
def direction():
    if request.method == 'POST':
        if request.form['button'] == 'Удалить':
            db.delete_line(request.form['num_dir'], 'direction_travel')
        if request.form['button'] == 'Добавить':
            db.insert_direction(request.form['start'], request.form['finish'], request.form['num_branch'])

    directions = db.select_all('direction_travel')
    stations = db.select_all('station')

    all_dir = []
    for i in range(len(directions)):
        dir = {}
        dir['id'] = directions[i][0]
        dir['branch'] = directions[i][3]
        for j in range(len(stations)):
            if directions[i][1] == stations[j][0]:
                dir['start'] = stations[j][1]
            if directions[i][2] == stations[j][0]:
                dir['finish'] = stations[j][1]
        all_dir.append(dir)

    return render_template('direction.html', title='Направления следования', menu=menu, all_dir=all_dir,
                           num_dir=len(directions))


@app.route("/contact")
def contact():
    return render_template('contact.html', title='Обратная связь', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
