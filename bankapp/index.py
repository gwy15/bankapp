import logging

from flask import Blueprint, render_template

from flask_login import login_required

logger = logging.getLogger(__name__)

bp = Blueprint('index', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index.html')
