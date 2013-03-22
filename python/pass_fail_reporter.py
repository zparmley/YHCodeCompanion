import subprocess
from testify import test_reporter

class PassFailReporter(test_reporter.TestReporter):

    def __init__(self, *args, **kwargs):
        self.all_passed = True
        super(PassFailReporter, self).__init__(*args, **kwargs)

    def test_complete(self, result):
        if result['failure']:
            self.all_passed = False

    def report(self):
        if self.all_passed:
            subprocess.call(["code_companion_send_message", "TESTIFY", "PASS"])
        else:
            subprocess.call(["code_companion_send_message", "TESTIFY", "FAIL"])

        return self.all_passed

def build_test_reporters(options):
    return [PassFailReporter(options)]
