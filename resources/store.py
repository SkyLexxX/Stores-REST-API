from flask_restful import Resource
from flask_jwt import jwt_required
from models.store_model import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'massage': "An store with name '{}' already exists".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occured creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'store deleted'}


class StoreList(Resource):
    def get(self):
        return {"stores": list(map(lambda store: store.json(), StoreModel.query.all()))}
