from flask import Blueprint

tickets=Blueprint('tickets',__name__)

from .import form,views,errors