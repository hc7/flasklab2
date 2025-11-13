from flask import Flask, Blueprint
from flask_restx import Api, Resource
app = Flask(__name__)
api = Api(app = app)
# описание главного блока нашего API http://127.0.0.1:5000/main/.
name_space = api.namespace('main', description='Main APIs')
@name_space.route("/")
class MainClass(Resource):
    def get(self):
        return {"status": "Got new data"}
    def post(self):
        return {"status": "Posted new data"}

# подключение API из другого файла
from part.part import api as partns1
api.add_namespace(partns1)
from part.parttmpl import api as partns2
from part.parttmpl import templ as templ
api.add_namespace(partns2)
app.register_blueprint(templ,url_prefix='/templ')
from part.list import name_space1 as listns1
api.add_namespace(listns1)

from part.list_db import name_space2 as listdbns1
api.add_namespace(listdbns1)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=7000)
