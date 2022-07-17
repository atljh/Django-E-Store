import pymongo
import environ

env = environ.Env()
environ.Env.read_env()


def init_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/",
                                 username=env("DATABASE_USER"), password=env("DATABASE_PASSWORD"))
    db = client[env("DATABASE_NAME")]
    return client, db


def get_by_id(product_id, collection_name='cart'):
    client, db = init_db()
    collection = db[collection_name]
    try:
        result = collection.find_one({'_id': product_id})
        client.close()
        return result
    except Exception as Exc:
        client.close()
        return Exc


def get_all_from_cart(collection_name='cart'):
    client, db = init_db()
    collection = db[collection_name]
    result = [item for item in collection.find()]
    client.close()
    return result


def write_cart(product_id, collection_name='cart'):
    client, db = init_db()
    collection = db[collection_name]
    result = collection.insert_one({
                                    '_id': product_id,
                                    'quantity': 1
                                    })
    client.close()
    return result



def update_cart(product_id, collection_name='cart'):
    client, db = init_db()
    collection = db[collection_name]
    item_quant = collection.find_one(product_id).get('quantity')
    item_to_update = get_by_id(product_id)
    result = collection.update_one(item_to_update,
                                   {'$set': {'_id': product_id, 'quantity': item_quant + 1}}, upsert=False)
    # result = collection.update_one({'_id': product_id, 'quantity': item_quant},
    #                                {'$set': {'_id': product_id, 'quantity': item_quant + 1}}, upsert=False)
    return result


def delete_from_cart(product_id, collection_name='cart'):
    client, db = init_db()
    collection = db[collection_name]
    item_quant = collection.find_one(product_id).get('quantity')
    if item_quant == 1:
        result = collection.delete_one({'_id': product_id})
        return result
    item_to_delete = get_by_id(product_id)
    result = collection.update_one(item_to_delete,
                                   {'$set': {'_id': product_id, 'quantity': item_quant - 1}}, upsert=False)
    return result


def delete_cart(collection_name='cart'):
    client, db = init_db()
    collection = db[collection_name]
    collection.drop()
