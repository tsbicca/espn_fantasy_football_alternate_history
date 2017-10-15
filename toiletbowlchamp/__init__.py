"""
The flask application package.
"""

from flask import Flask
from flask_bootstrap3 import Bootstrap

app = Flask(__name__)
Bootstrap(app)

import ToiletBowlChamp.views


