from flask import render_template, request
from manage import app, db, mongo, Individual_GIS, Individual_EC, Individual_NHIA


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []

    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if first_name and last_name:
            results_EC = Individual_EC.query.filter_by(first_name=first_name, last_name=last_name).all()
            results_GIS = Individual_GIS.query.filter_by(first_name=first_name, last_name=last_name).all()
            results_NHIA = Individual_NHIA.query.filter_by(first_name=first_name, last_name=last_name).all()

            citizens = mongo.db.individual_DVLA
            results_DVLA = []
            for c in citizens.find():
                results_DVLA.append(
                    {'first_name': c['first_name'], 'middle_name': c['middle_name'], 'last_name': c['last_name'],
                     'age': c['age']})

            return render_template('results.html', results_EC=results_EC, results_GIS=results_GIS,
                                   results_NHIA=results_NHIA, results_DVLA=results_DVLA)
        else:
            errors = {"error": "The request payload is not in JSON format"}

    return render_template('home.html', errors=errors)


@app.route('/results', methods=['GET', ])
def results():
    return render_template('results.html')


if __name__ == "__main__":
    citizen_1 = Individual_EC(
        first_name="Kwame",
        middle_name="Atiemo",
        last_name="Asare",
        age=22
    )
    citizen_2 = Individual_GIS(
        first_name="Kwame",
        middle_name="Atiemo",
        last_name="Asare",
        age=22
    )
    citizen_3 = Individual_NHIA(
        first_name="Kwame",
        middle_name="Atiemo",
        last_name="Asare",
        age=22
    )
    citizen_4 = {
        "first_name": "Yaw",
        "middle_name": "Osei",
        "last_name": "Appiah",
        "age": "25",
    }

    db.session.add(citizen_1, citizen_2, citizen_3)  # Adds new User record to database
    db.session.commit()
    mongo.db.individual_DVLA.insert(citizen_4)

    app.run()
