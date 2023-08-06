import threading
import os
import unittest

try:
    if int(os.environ['ONNC_TESTMODE']):
        import sys
        sys.path.append('../')
except:
    pass

from onnc.bench import Workspace

onnc_test_key = os.environ['ONNC_APIKEY']


class GlobalExceptionWatcher(object):

    def _store_excepthook(self):
        '''
        Uses as an exception handlers which stores any uncaught exceptions.
        '''
        formated_exc = self.__org_hook()
        self._exceptions.append(formated_exc)
        return formated_exc

    def __enter__(self):
        '''
        Register us to the hook.
        '''
        self._exceptions = []
        self.__org_hook = threading._format_exc
        threading._format_exc = self._store_excepthook

    def __exit__(self, type, value, traceback):
        '''
        Remove us from the hook, assure no exception were thrown.
        '''
        threading._format_exc = self.__org_hook
        if len(self._exceptions) != 0:
            tracebacks = os.linesep.join(self._exceptions)
            raise Exception('Exceptions in other threads: %s' % tracebacks)


class TestCompileMulti(unittest.TestCase):

    def compile(self, model, samples, input_name, board, ram_size, output):
        print(onnc_test_key)
        with Workspace(onnc_test_key) as ws:
            res = ws.upload_model(model, samples, input_name=input_name)
            print("UPLOAD", res)
            res = ws.compile(board=board, ram_size=ram_size)
            print("COMPILE", res)
            res = ws.download(output, unzip=True)
            print("DOWNLOAD", res)

    def test_multi_thread(self):
        n_requests = 20
        threads = []
        with GlobalExceptionWatcher():
            for i in range(n_requests):
                t = threading.Thread(
                    target=self.compile,
                    args=(
                        "../examples/serialized/resources/onnx_pb/model.onnx",
                        "../examples/serialized/resources/onnx_pb/samples.pb",
                        "input_1",
                        "NUMAKER_IOT_M487",
                        65536,
                        "./loadable.zip",
                    ))
                threads.append(t)
                threads[i].start()
            for i in range(n_requests):
                threads[i].join()

        print(f"Done {n_requests} requests")


if __name__ == '__main__':
    unittest.main()
