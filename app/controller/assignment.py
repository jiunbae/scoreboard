from app.models import Assignment as assignment

class Assignment():
    @staticmethod
    def index():
        pass

    @staticmethod
    def show():
        pass

    @staticmethod
    def destroy():
        pass

    @staticmethod
    def create():
        pass


# @app.route('/assignments')
# def assignments():
#     return render_template('list.html', assignments=get_assignments())

# @app.route('/assignment/<pid>')
# def assignment(pid):
#     return render_template('assignment.html', pid=pid, assignment=get_assignment(int(pid)))
