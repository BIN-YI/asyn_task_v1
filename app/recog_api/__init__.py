from flask import Blueprint

#flask很常有這種奇怪的init
recog_api = Blueprint('recog_api', __name__)

#拜訪允許
from . import recog_apis