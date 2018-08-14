from os.path import join

from werkzeug.utils import secure_filename

from app import app
from app.controller import Controller
from app.models import Submission as submission

class Submission(Controller):
    model = submission

    @classmethod
    def write_file(cls, file) -> None:
        filename = secure_filename(file.filename)
        file.save(join(app.config['UPLOAD_FOLDER'], filename))
        return filename
