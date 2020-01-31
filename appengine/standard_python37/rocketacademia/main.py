# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import datetime

from flask import Flask, request, render_template, redirect, url_for
from google.cloud import datastore

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/descuento')
def descuento():
    return render_template('descuento.html')

@app.route('/cupon')
def cupon():
    return render_template('cupon.html')

@app.route('/obtener/descuento', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')

        client = datastore.Client('rocketacademia')

        query = client.query(kind='PROSPECTOS_CLIENTES')
        query.add_filter('CORREO', '=', correo)
        results = list(query.fetch())
        if len(results) > 1:
            return render_template("cupon_existente.html",correo=correo)

        with client.transaction():
            incomplete_key = client.key('PROSPECTOS_CLIENTES')

            prospecto = datastore.Entity(key=incomplete_key)

            prospecto.update({
            'CORREO': correo,
            'NOMBRE': nombre,
            'TELEFONO': telefono,
            'FECHA':datetime.datetime.now()
            })

            client.put(prospecto)

        return render_template("cupon.html",form=[],nombre=nombre)

    return render_template("descuento.html")

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
