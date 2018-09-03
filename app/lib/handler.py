import argparse
from subprocess import Popen, PIPE, STDOUT
from os.path import join

import numpy as np

class Handler:
    @classmethod
    def scoring(cls, instance):
        from app import Session
        from app.lib.file import File
        from app.controller import Challenge
        from app.controller import Submission
        process = Popen(['python', 'app/lib/handler.py',
                        str(File(Submission.model.directory, instance.file)),
                        str(File(Challenge.model.directory, instance.challenge.label)),
                        str(instance.challenge.cate)],
                        stdout=PIPE,
                        stderr=STDOUT)
        result, *_ = process.communicate()
        try:
            instance.score = float(result.decode('utf-8'))
            instance.result = 'done'
        except Exception as e:
            instance.result = result
        instance.state = 'done'
        Session.commit()

    @classmethod
    def evaluate(cls, filename: str, labelname: str, cate: str) -> float:
        from metric import Metric
        from file import File

        # TODO: assert index match
        label = File.read_csv(labelname)
        test = File.read_csv(filename)

        if np.size(label, 0) != np.size(test, 0):
            print ("Instance number mismatch")
        else:
            result = Metric.__subclasses__()[cate]()(label, test)
            print (result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        help="submission file name",
                        type=str)
    parser.add_argument("labelname",
                        help="assignment label name",
                        type=str)
    parser.add_argument("cate",
                        help="assignment category",
                        type=int)
    args = parser.parse_args()
    Handler.evaluate(args.filename, args.labelname, int(args.cate))
