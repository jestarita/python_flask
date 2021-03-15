from flask import  Flask, request,jsonify
from flask_sqlalchemy import  SQLAlchemy
from flask_marshmallow import  Marshmallow



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mysqlflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    estado = db.Column(db.Integer)


    def __init__(self,nombre,last_name,estado):
        self.nombre = nombre
        self.last_name = last_name
        self.estado = estado
db.create_all()

class  UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'last_name')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

@app.route('/usuarios', methods=['Get'])
def listado():
    print (request.json)
    return 'obtenido desde backend'
@app.route('/Save', methods=['POST'])
def guardar():

    name = request.json['nombre']
    last_name = request.json['apellidos']
    estado = request.json['estado']

    usu =  Usuario(name,last_name,estado)
    db.session.add(usu)
    db.session.commit()

    return usuario_schema.jsonify(usu)

@app.route('/Listado', methods=['Get'])
def getUsers():
    all_users = Usuario.query.all()
    listado = usuarios_schema.dump(all_users)
    return jsonify(listado)

@app.route('/usuario/<id>', methods=['Get'])
def getUser(id):
    user = Usuario.query.get(id)
    usuario_resp = usuario_schema.dump(user)
    return jsonify(usuario_resp)

@app.route('/Update/<id>', methods=['PUT'])
def actualizar(id):

    user = Usuario.query.get(id)

    name_get = request.json['nombre']
    last_name_get = request.json['apellidos']
    estado_get = request.json['estado']

    user.nombre = name_get
    user.last_name = last_name_get
    user.estado = estado_get

    db.session.commit()

    return usuario_schema.jsonify(user)


@app.route('/Eliminar/<id>', methods=['DELETE'])
def eliminar(id):

    user = Usuario.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return usuario_schema.jsonify(user)

@app.route('/', methods=['GET'])
def Index():
    return 'Api de aprendizaje flask'

if __name__ == '__main__':
    app.run(debug=True)