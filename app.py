from flask import Flask, json, request, g, session, jsonify

from src.middleware.cors import cors
from src.database.database import init_db
from config import config

from src.database.controller import *

from datetime import datetime, timedelta


def init_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    # app에 뭔가 더 추가하고 싶은게 있으면 여기에 추가
    cors.init_app(app)

    return app

app = init_app()
engine, get_db = init_db(config.DATABASE_URI)


# 연결이 끊어질때 db close
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/status')
def status():
    return json.jsonify({'status': 'ok'}), 200

@app.route('/api/taxi_info/create', methods=["POST"])
def create_taxi_group():
    is_authenticated = bool(session("is_authenticated", False))
    if not is_authenticated:
        return jsonify({"msg": "권한 없음"}), 403
    
    data = request.get_json()
    start_time = data.get("start_time", "")
    end_position = data.get("end_position", "")
    total_people = data.get("total_people", "")
    start_position = data.get("start_position", "")

    creator_nickname = session.get("nickname", "")
    creator_id = session.get("user_id", "")
    new_pool = create_taxi_pool(get_db(), start_position, end_position, total_people, start_time, creator_nickname, creator_id)
    return jsonify({"id": new_pool.id}), 200

@app.route("/api/taxi_info", methods=["GET"])
def get_taxi_info():
    day = request.get("day", 6)
    if day > 6:     # for unexpected input
        day = 6
    info = []
    info = select_taxi_pools_by_day(get_db(), datetime.now()-timedelta(day), datetime.now())
    
    if len(info) == 0:
        return jsonify({"msg": "팟이 없어요"}), 404
    return jsonify({"taxi_list": info}), 200

@app.route("/api/taxi_info/<id>", methods=["GET"])
def get_taxi_info_by_id(id):
    id = int(id)
    '''
	start_position : string
	end_position : string
	total_people : int
	participation_num : int
	start_time : datetime.Datetime
	creator : string	
	day : int(min = 0, max = 6)
    '''
    info = get_taxi_pool_id(get_db(), id)
    res = {
        "start_position": info.start_position,
        "end_position": info.end_position,
        "total_people": info.total_people,
        "participation_num": count_pool_members_by_taxi_id(get_db(), info.id),
        "start_time": info.start_time,
        "creator_nickname": info.creator_nickname
    }
    return jsonify(res), 200

@app.route("/api/taxi_info/participate", methods=["POST"])
def request_participation():
    is_authenticated = bool(session("is_authenticated", False))
    nickname = session.get("nickname", "")
    if not is_authenticated:
        return jsonify({"msg": "권한 없음"}), 403

    data = request.get_json()
    user_id = data.get("user_id", "")
    taxi_id = data.get("taxi_id", "")

    if get_taxi_pool_id(get_db(), taxi_id)==None:
        return jsonify({"msg": "해당 택시팟이 없음"}), 404
    else:
        res = create_pool_member(get_db(), taxi_id, user_id)
        if res != None:
            return jsonify({}), 200

@app.route("/api/taxi_info/participate", methods=["GET"])
def is_participated():
    data = request.get_json()
    user_id = data.get("user_id", "")
    taxi_id = data.get("taxi_id", "")
    member = select_pool_member_by_taxi_user_id(get_db(), user_id, taxi_id)
    if member == None:
        is_participated = False
    else:
        is_participated = True
    return jsonify({"is_participated": is_participated}), 200


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=13242)