import json
from flask_restx import Namespace, Resource, fields
from flask_restx import reqparse
import logging

name_space1 = Namespace('list_db', description='List API')

logger = logging.getLogger('gunicorn.error')

# Content of items.json will look like:
"""
{
    "id00000001": {
        "desc": "component3",
        "vendor": "vendor2",
        "price": 0.0,
        "quantity": 1
    },
    "id00000002": {
        "desc": "component2",
        "vendor": "vendor3",
        "price": 0.0,
        "quantity": 1
    },
    ...
}
"""

try:
    # Load from JSON (in your app startup)
    with open('items.json', 'r') as f:
        ITEMS = json.load(f)
        logger.info("Loaded ITEMS from items.json")
except Exception as e:
    logger.error(f"Error loading items: {e}")
    ITEMS = {
        "id00000001": {"desc": "component3", "vendor": "vendor2", "price": 0.0, "quantity": 1},
        "id00000002": {"desc": "component2", "vendor": "vendor3", "price": 0.0, "quantity": 1},
        "id00000003": {"desc": "component1", "vendor": "vendor1", "price": 0.0, "quantity": 1},
        "id00000004": {"desc": "component2", "vendor": "vendor1", "price": 0.0, "quantity": 1},
        "id00000005": {"desc": "component4", "vendor": "vendor3", "price": 0.1, "quantity": 2},
    }

def save_items():
    """Save items to JSON file"""
    try:
        with open('items.json', 'w') as f:
            json.dump(ITEMS, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved {len(ITEMS)} items to 'items.json'")
        return True
    except Exception as e:
        logger.error(f"Error saving items: {e}")
        return False


item = name_space1.model(
    "Item", {
    'desc': fields.String(required=True, description='The description details'),
    'vendor': fields.String(required=True, description='The vendor details'),
    'price': fields.Float(required=False, description='Item Price'),
    'quantity': fields.Integer(required=False, description='Items number'),
    }
)

listed_item = name_space1.model(
    "ListedItem",
    {
        "id": fields.String(readonly=True, description="The item ID"),
        "item": fields.Nested(item, description="The Item"),
    },
)

calculate = name_space1.model(
    "Summarize",
    {
        "function": fields.String(readonly=True, description="The function name"),
        "result": fields.String(readonly=True, description="The result"),
    },
)

def abort_if_todo_doesnt_exist(id):
    if id not in ITEMS:
        name_space1.abort(404, "Item {} doesn't exist".format(id))

# parser = name_space1.parser()
# parser.add_argument(
#     "id", type=str, required=True, help="The item details", location="form"
# )

add_parser = name_space1.parser()
add_parser.add_argument(
    "new_id", type=int, required=False, help="The item details"
)
add_parser.add_argument(
    "desc", type=str, required=False , help="The item details"
)
add_parser.add_argument(
    "vendor", type=str, required=False, help="The item details"
)

add_parser.add_argument(
    "price", type=float, required=False, help="The item details"
)

add_parser.add_argument(
    "quantity", type=int, required=False, help="The item details"
)

def get_next_id():
    if not ITEMS:
        return "id00000001"
    
    # Extract numeric parts and find max
    max_id = max(int(item_id[2:]) for item_id in ITEMS.keys())
    next_id_num = max_id + 1
    return f"id{next_id_num:08d}"

# Usage
# new_id = get_next_id()
# ITEMS[new_id] = {"desc": "new_component", "vendor": "new_vendor", "price": 0.0, "quantity": 1}


@name_space1.route("/<string:id>")
@name_space1.doc(responses={404: "Item not found"}, params={"id": "The Item ID"})
class Todo(Resource):
    """Show a single item and lets you delete them"""

    @name_space1.doc(description="id should be in {0}".format(", ".join(ITEMS.keys())))
    @name_space1.marshal_with(item)
    def get(self, id):
        """Fetch a given resource"""
        abort_if_todo_doesnt_exist(id)
        logger.info(f" {ITEMS[id]}")
        return ITEMS[id]

    @name_space1.doc(responses={204: "Item deleted"})
    def delete(self, id):
        """Delete a given resource"""
        abort_if_todo_doesnt_exist(id)
        del ITEMS[id]
        save_items()
        return "", 204

    @name_space1.doc(parser=add_parser)
    @name_space1.marshal_with(item)
    def put(self, id):
        """Update a given resource"""
        args = add_parser.parse_args()
        if args["new_id"]:
            if args["new_id"] >= 0:
                add_id = "id%08d" % args["new_id"]
        else:
            add_id = get_next_id() # id # should be generate new uniq id here
        if id in ITEMS:
            logger.debug(" Copy origin values to new item")
            new_desc = args["desc"] if args["desc"] else ITEMS[id]['desc']
            new_vendor = args["vendor"] if args["vendor"] else ITEMS[id]['vendor']
            new_quantity = args["quantity"] if args["quantity"] else ITEMS[id]['quantity']
            new_price = args["price"] if args["price"] else ITEMS[id]['price']
        else:
            logger.debug(" Set default values for new item")
            new_desc = args["desc"] if args["desc"] else "Description"
            new_vendor = args["vendor"] if args["vendor"] else "Vendor"
            new_quantity = args["quantity"] if args["quantity"] else 1
            new_price = args["price"] if args["price"] else 1.0

        item = {"desc": new_desc, "vendor" : new_vendor, "price" : new_price, "quantity" : new_quantity}
        logger.info(f" {add_id} {item}")
        ITEMS[add_id] = item
        save_items()
        return item

reqop = reqparse.RequestParser()
# добавление аргументов, передаваемых запросом GET
# например GET http://127.0.0.1:5000/list/add?len=7&val=%D0%BB%D0%B4%D1%80%D0%BE%D0%BB%D0%BE%D1%80
#reqp.add_argument('len', type=int, required=False)

reqop.add_argument('id', type=str, required=False)
reqop.add_argument('desc', type=str, required=False)
reqop.add_argument('vendor', type=str, required=False)
reqop.add_argument('price', type=float, required=False)
reqop.add_argument('quantity', type=int, required=False)
reqop.add_argument('sort', type=str, required=False)
reqop.add_argument('evaluate', type=str, required=False)

column = {'desc','vendor','price','quantity'}
sort_order = ['desc','rdesc','vendor','rvendor','price','rprice','quantity','rquantity']
sort_revers = {'desc':False,'rdesc':True,'vendor':False,'rvendor':True,'price':False,'rprice':True,'quantity':False,'rquantity':True}


@name_space1.route("/op")
class MakeUp(Resource):
    @name_space1.doc("")
    # маршалинг данных в соответствии с моделью minmax
    @name_space1.expect(reqop)
    @name_space1.marshal_with(listed_item)
    def get(self):
        """Получение значения из базы"""
        # global allarray
        args = reqop.parse_args()
        if args["id"]:
            abort_if_todo_doesnt_exist(args["id"])
            return [{"id": args["id"], "item" : ITEMS[args["id"]]}]
        else:
            
            r = {id : data for id, data in ITEMS.items()}
            for c in column:
                if args[c]:
                    r = {id : data for id, data in r.items() if data[c] == args[c]}
            if args["sort"]:
                sort_option = args["sort"].split(":")
                sort_option.reverse()
                logger.debug(f"{sort_option}")
                # Sort by vendor descending (string), then price ascending (numeric)
                # Two-step approach
                items_list = list(r.items())

                for s in sort_option:
                    if s in sort_order:
                        items_list.sort(key=lambda x: x[1][s],reverse=sort_revers[s])  # Secondary sort first
                r = dict(items_list)            
            return [{"id": id, "item": data} for id, data in r.items()]

    # @name_space1.doc(parser=reqop)
    # @name_space1.marshal_with(listed_item, code=204)
    # def post(self):
    #     """Create a todo"""
    #     args = reqop.parse_args()
    #     todo_id = "todo%08d" % (len(ITEMS) + 1)
    #     ITEMS[todo_id] = {"desc": args["desc"], "vendor" : args["vendor"], "price" : args["price"], "quantity" : args["quantity"]}
    #     return ITEMS[todo_id], 204

reqfun = reqparse.RequestParser()

reqfun.add_argument('desc', type=str, required=False)
reqfun.add_argument('vendor', type=str, required=False)

@name_space1.route("/calc")
@name_space1.doc(responses={404: "Item not found"})
class calc(Resource):
    # @name_space1.doc("")
    # маршалинг данных в соответствии с моделью minmax
    @name_space1.expect(reqfun)
    @name_space1.marshal_with(calculate)
    @name_space1.doc(responses={404: "Item not found"})
    def get(self):
        """Calculate interesting values"""
        args = reqfun.parse_args()
            
        r = {id : data for id, data in ITEMS.items()}
        for c in column:
            if c in args and args[c]:
                r = {id : data for id, data in r.items() if data[c] == args[c]}
                if not r:
                    name_space1.abort(404, "Item '{}' doesn't exist".format(args[c]))
                    #return [], 404
                    #name_space1.abort(204, "Items for {} don't exist".format(args[c]))
        result = {}
        result['quantity_minumum'] = str(min(data['quantity'] for data in r.values()))
        result['quantity_maximum'] = str(max(data['quantity'] for data in r.values()))
        result['quantity_total'] = str(sum(data['quantity'] for data in r.values()))
        result['price_max'] = str(max(data['price'] for data in r.values()))
        result['price_min'] = str(min(data['price'] for data in r.values()))
        result['price_avg'] = str(sum(item['price'] for item in r.values()) / len(r) if r else 0.0)

        return [{"function": id, "result": data} for id, data in result.items()]
