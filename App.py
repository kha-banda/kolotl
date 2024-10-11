from flask import Flask, redirect, render_template, request, url_for, session
#from flask_mysqldb import MySQL
import pymysql
import plotly.graph_objs as go


app = Flask(__name__)
static_folder='static'

#coneccion con mysql
#connection = pymysql.connect(host='localhost',
#                             user='root',
#                             password='',
#                             database='db_kolotl',
#                             )

#Definicion de los gráficos

@app.route('/')
def Index():
    #cur = connection.cursor()
    #cur.execute('SELECT * FROM users')
    #data = cur.fetchall()
    #print(data)
    #return render_template('index.html', datos = data)
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        rol_var = request.form['ID']
        correo_var = request.form['Email']
        name_var = request.form['Nombre']
        sql_var = connection.cursor()
        sql_var.execute('INSERT INTO users (role_id, email, first_name) VALUES (%s, %s, %s)' ,
                        (rol_var, correo_var, name_var))
        sql_var.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delate_contact/<string:id>')
def delate_contact(id):
    var_cur = connection.cursor()
    var_cur.execute('DELETE FROM users WHERE id={0}'.format(id))
    connection.commit()
    return redirect(url_for ('Index'))

@app.route('/edit')
def edit_contact():
    return 'editando contacto'

#ligas a las páginas de kolotl

@app.route('/Estadisticas')
def estadisticas():
    x_data=[1,2,3,4,5,6,7,8,9,10,11,12]
    y_data=[10,15,20,12,78,30,13,34,23,56,12,89]
    trace = go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='Datos Ejemplo')
    data = [trace]
    layout = go.Layout(title='No. Especies Encontradas 2023', xaxis=dict(title='Meses'), yaxis=dict(title='No. Especies'))
    fig = go.Figure(data=data, layout=layout)
    # Convierte el gráfico a JSON
    graph_json = fig.to_json()
    # tipos de gráficas tenemos scatter por puntos, line, bar, area, pie, bubble, heatmap, box, funnel
    #GRáfico 1 datos de número de alacranes
    x1_data=[2020,2021,2022,2023]
    y2_data=[100,78,45,200]
    trace1 = go.Scatter(x=x1_data, y=y2_data, mode='lines+markers', name='Registro de alacranes')
    data1 = [trace1]
    layout1 = go.Layout(title='Especies por año encontradas', xaxis=dict(title='Años'), yaxis=dict(title='No. de Especies'))
    fig1 = go.Figure(data=data1, layout=layout1)
    # Convierte el gráfico a JSON
    graph2_json = fig1.to_json()   
    
    #gráfica con barras
    data_barras ={ 'anos': ['2018','2019','2020','2021'],
                    'Publica':[10, 40, 30, 4]
                }  
    return render_template('index-1.html', graphJSON=graph_json, graph2JSON=graph2_json, data_barras=data_barras)

@app.route('/Galeria')
def galeria():
    return render_template('index-2.html')

@app.route('/Acerca')
def acerca():
    return render_template('index-3.html')

@app.route('/Contacto')
def contacto():
    return render_template('index-4.html')

app.run(debug=True)