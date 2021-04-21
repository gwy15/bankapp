# https://flask-wtf.readthedocs.io/en/stable/quickstart.html
from .. import bp


@bp.route('/register', methods=['GET'])
def register():
    pass
