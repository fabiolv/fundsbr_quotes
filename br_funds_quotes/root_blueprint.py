from flask import Blueprint, jsonify

root_blueprint = Blueprint('root_bluprint', __name__)

@root_blueprint.route('/', methods=['GET'])
def root():
    return jsonify(msg='This is the root / endpoint... and there is nothing here...'
        , version = 'v1'
    )