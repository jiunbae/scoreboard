from app import app
from app.view import Router
from app.controller import Assignment as controller

assignment = Router('assignment')

assignment.route('/').get = controller.index
assignment.route('/').post = controller.create

assignment.route('/<aid>').get = controller.show
assignment.route('/<aid>').delete = controller.destroy
