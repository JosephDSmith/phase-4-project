#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session, jsonify, abort
from flask_restful import Resource
from werkzeug.exceptions import NotFound

# Local imports
from config import app, db, api, bcrypt
from models import User, Butterfly, Plant, Tag


class Signup(Resource):
    def post(self):
        form_json = request.get_json()
        new_user = User()
        for attr in form_json:
            setattr(new_user, attr, form_json[attr])
        # new_user = User(name=form_json['name'], email=form_json['email'])
        new_user.password_hash = form_json["password"]
        db.session.add(new_user)
        db.session.commit()
        # Store the user ID in the session
        session["user_id"] = new_user.id

        response = make_response(new_user.to_dict(), 201)
        return response


api.add_resource(Signup, "/signup")


class Login(Resource):
    def post(self):
        json = request.get_json()
        try:
            user = User.query.filter_by(name=json["name"]).first()
            if user.authenticate(json["password"]):
                session["user_id"] = user.id
                response = make_response(user.to_dict(), 200)
                return response
        except:
            abort(401, "Incorrect Username or Password")


api.add_resource(Login, "/login")


class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        response = make_response("", 204)
        return response


api.add_resource(Logout, "/logout")


class AuthorizedSessions(Resource):
    def get(self):
        try:
            user = User.query.filter_by(id=session["user_id"]).first()
            response = make_response(user.to_dict(), 200)
            return response
        except:
            abort(401, "Unauthorized")


api.add_resource(AuthorizedSessions, "/authorized")


class Butterflies(Resource):
    def get(self):
        butterfly_list = [b.to_dict() for b in Butterfly.query.all()]
        response = make_response(
            butterfly_list,
            200,
        )

        return response

    def post(self):
        form_json = request.get_json()
        try:
            new_butterfly = Butterfly(
                name=form_json["name"],
                image=form_json["image"],
                user_id=session["user_id"],
            )
        except ValueError as e:
            abort(422, e.args[0])

        db.session.add(new_butterfly)
        db.session.commit()

        response = make_response(
            new_butterfly.to_dict(),
            201,
        )
        return response


api.add_resource(Butterflies, "/butterflies")


class ButterflyByID(Resource):
    def get(self, id):
        butterfly = Butterfly.query.filter_by(id=id).first()
        if not butterfly:
            raise NotFound
        response = make_response(butterfly.to_dict(), 200)

        return response

    def patch(self, id):
        butterfly = Butterfly.query.filter_by(id=id).first()
        if not butterfly:
            raise NotFound
        if butterfly.user_id != session['user_id']:
            abort(401, "Unauthorized")

        form_json = request.get_json()
        for attr in form_json:
            setattr(butterfly, attr, form_json[attr])

        db.session.add(butterfly)
        db.session.commit()

        response = make_response(butterfly.to_dict(), 200)
        return response

    def delete(self, id):
        butterfly = Butterfly.query.filter_by(id=id).first()
        if not butterfly:
            raise NotFound
        if butterfly.user_id != session['user_id']:
            abort(401, "Unauthorized")
        db.session.delete(butterfly)
        db.session.commit()

        response = make_response("", 204)

        return response


api.add_resource(ButterflyByID, "/butterflies/<int:id>")


class Plants(Resource):
    def get(self):
        plant_list = [b.to_dict() for b in Plant.query.all()]
        response = make_response(
            plant_list,
            200,
        )

        return response

    def post(self):
        form_json = request.get_json()
        try:
            new_plant = Butterfly(
                name=form_json["name"],
                genus_species=form_json["genus_species"],
                growing_zone=session["growing_zone"],
            )
        except ValueError as e:
            abort(422, e.args[0])

        db.session.add(new_plant)
        db.session.commit()

        response = make_response(
            new_plant.to_dict(),
            201,
        )
        return response


api.add_resource(Plants, "/plants")


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            raise NotFound
        response = make_response(plant.to_dict(), 200)

        return response

    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
                raise NotFound
        if plant.user_id != session['user_id']:
            abort(401, "Unauthorized")
        else:
            form_json = request.get_json()
            for attr in form_json:
                setattr(plant, attr, form_json[attr])

            db.session.add(plant)
            db.session.commit()

            response = make_response(plant.to_dict(), 200)
            return response

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            raise NotFound
        if plant.user_id != session['user_id']:
            abort(401, "Unauthorized")
        db.session.delete(plant)
        db.session.commit()

        response = make_response("", 204)

        return response


api.add_resource(PlantByID, "/plants/<int:id>")


class ButterflyTag(Resource):
    def post(self, id):
        json = request.get_json()
        tag = Tag.query.filter_by(name=json["name"]).first()
        if not tag:
            tag = Tag(name=json["name"])
        butterfly = Butterfly.query.filter_by(id=id).first()
        butterfly.tags.append(tag)
        db.sesion.add(butterfly)
        db.session.commit()
        response = make_response(butterfly.to_dict(), 201)
        return response


api.add_resource(ButterflyTag, "/butterflies/<int:id>/tag")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
