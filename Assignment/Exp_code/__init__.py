from flask import Flask
from Exp_code.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from Exp_code import routes