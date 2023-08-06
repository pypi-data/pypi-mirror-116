from onnc.workspace import Workspace
import unittest


class TestWorkspace(unittest.TestCase):
    def test_all_pipeline(self):

        with Workspace() as ws:

            ws.upload_model('./resources/test_model.h5',
                            './resources/test_model.h5',
                            input_name='input1')

            res = ws.compile(board='NUMAKER_IOT_M487', ram_size=65536)
            self.assertEqual(res['success'], True)
            self.assertEqual(type(res['report']['ram']), int)

            res = ws.download('./loadable', unzip=True)
            self.assertEqual(res['success'], True)

    def test_all_pipeline_folder(self):
        with Workspace() as ws:
            ws.upload_model('./resources/', './resources/',
                            input_name='input1')

            res = ws.compile(board='NUMAKER_IOT_M487', ram_size=65536)
            self.assertEqual(res['success'], True)
            self.assertEqual(type(res['report']['ram']), int)

            res = ws.download('./loadable', unzip=True)
            self.assertEqual(res['success'], True)

    def test_all_pipeline_board(self):

        with Workspace() as ws:
            ws.upload_model('./resources/test_model.h5',
                            './resources/test_model.h5',
                            input_name='input1')
            res = ws.compile(board='NUMAKER_IOT_M487')
            self.assertEqual(res['success'], True)
            self.assertEqual(type(res['report']['ram']), int)

            res = ws.download('./loadable', unzip=True)
            self.assertEqual(res['success'], True)
            # untar


if __name__ == '__main__':
    unittest.main()
