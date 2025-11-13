from flask_restx import Namespace, Resource, fields
name_space1 = Namespace('list', description='List API')
# определение модели данных массива
list_ = name_space1.model('list', {
    'len': fields.String(required=True, description='Size of array'),
    'array': fields.List(fields.String,required=True, description='Some array'),
})
# массив, который хранится в оперативной памяти
allarray = ['1']
#name_space1 = api.namespace('list', description='list APIs')
@name_space1.route("/")
class ListClass(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(list_)
    def get(self):
        """Получение всего хранимого массива"""
        return {'len': str(len(allarray)), 'array': allarray}

    @name_space1.doc("")
    # ожидаем на входе данных в соответствии с моделью list_
    @name_space1.expect(list_)
    # маршалинг данных в соответствии с list_
    @name_space1.marshal_with(list_)
    def post(self):
        """Создание массива/наше описание функции пост"""
        global allarray
        # получить переданный массив из тела запроса
        allarray = name_space1.payload['array']
        # возвратить новый созданный массив клиенту
        return {'len': str(len(allarray)), 'array': allarray}

# модель данные с двумя параметрами строкового типа
minmax = name_space1.model('minmax', {'min':fields.String, 'max':fields.String}, required=True, description='two values')
# url 127.0.0.1/list/mimmax
@name_space1.route("/minmax")
class MinMaxClass(Resource):
    @name_space1.doc("")
    # маршалинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(minmax)
    def get(self):
        """Получение максимума и минимума массива"""
        global allarray
        return {'min': min(allarray), 'max': max(allarray)}

from flask_restx import reqparse
from random import random
reqp = reqparse.RequestParser()
# добавление аргументов, передаваемых запросом GET
# например GET http://127.0.0.1:5000/list/makerand?len=7&minval=1&maxval=12
reqp.add_argument('len', type=int, required=False)
reqp.add_argument('minval', type=float, required=False)
reqp.add_argument('maxval', type=float, required=False)
@name_space1.route("/makerand")
class MakeArrayClass(Resource):
    @name_space1.doc("")
    # маршалинг данных в соответствии с моделью minmax
    @name_space1.expect(reqp)
    @name_space1.marshal_with(list_)
    def get(self):
        """Возвращение массива случайных значений от min до max"""
        args = reqp.parse_args()
        array = [random()*(args['maxval']-args['minval'])+args['minval'] for i in range(args['len'])]
        return {'len': args['len'], 'array': array}

reqp = reqparse.RequestParser()
# добавление аргументов, передаваемых запросом GET
# например GET http://127.0.0.1:5000/list/add?len=7&val=%D0%BB%D0%B4%D1%80%D0%BE%D0%BB%D0%BE%D1%80
#reqp.add_argument('len', type=int, required=False)
reqp.add_argument('val', type=str, required=False)
@name_space1.route("/add")
class MakeUp(Resource):
    @name_space1.doc("")
    # маршалинг данных в соответствии с моделью minmax
    @name_space1.expect(reqp)
    @name_space1.marshal_with(list_)
    def get(self):
        """Добавление значения в массив"""
        global allarray
        args = reqp.parse_args()
        #array = [random()*(args['maxval']-args['minval'])+args['minval'] for i in range(args['len'])]
        allarray.append(args['val'])
        return {'len': str(len(allarray)), 'array': allarray}

# list_db = name_space1.model('list_db', {
#     'len': fields.String(required=True, description='Size of array'),
#     'array': fields.List(fields.String,required=True, description='Some array'),
# })

# reqop = reqparse.RequestParser()
# # добавление аргументов, передаваемых запросом GET
# # например GET http://127.0.0.1:5000/list/add?len=7&val=%D0%BB%D0%B4%D1%80%D0%BE%D0%BB%D0%BE%D1%80
# #reqp.add_argument('len', type=int, required=False)
# reqop.add_argument('id', type=int, required=False)
# reqop.add_argument('desc', type=str, required=True)
# reqop.add_argument('vendor', type=str, required=True)
# reqop.add_argument('price', type=float, required=False)
# reqop.add_argument('quentity', type=int, required=False)
# @name_space1.route("/op")
# class MakeUp(Resource):
#     @name_space1.doc("")
#     # маршалинг данных в соответствии с моделью minmax
#     @name_space1.expect(reqop)
#     @name_space1.marshal_with(list_db)
#     def get(self):
#         """Добавление значения в массив"""
#         global allarray
#         args = reqop.parse_args()
#         #array = [random()*(args['maxval']-args['minval'])+args['minval'] for i in range(args['len'])]
#         allarray.append(args['val'])
#         return {'len': str(len(allarray)), 'array': allarray}