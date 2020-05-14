from flask import Blueprint

#flask很常有這種奇怪的init
api = Blueprint('api', __name__)

#拜訪允許
from . import apis