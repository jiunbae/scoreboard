from app import app
from app.view import Router
from app.controller import Assignment as controller

assignment = Router('assignment')

assignment.route('/').GET = controller.index
assignment.route('/').POST = controller.create

assignment.route('/<aid>').GET = controller.show
assignment.route('/<aid>').DELETE = controller.destroy
