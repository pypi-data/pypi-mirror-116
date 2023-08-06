import argparse
import os

try:
    if int(os.environ['ONNC_TESTMODE']):
        import sys
        sys.path.append('../')
except:
    pass

from onnc.bench import Workspace


def compile(model, samples, input_name, board, ram_size, output):
    with Workspace() as ws:
        res = ws.upload_model(model, samples, input_name=input_name)
        print(res)
        res = ws.compile(board=board, ram_size=ram_size)
        print(res)
        res = ws.download(output, unzip=True)
        print(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Pack npy files within a given directory into a pb file.')
    parser.add_argument('model',
                        type=str,
                        help='a file/directory path of model')
    parser.add_argument('samples',
                        type=str,
                        help='a file/directory path of samples')

    parser.add_argument('--output',
                        type=str,
                        default='./loadable.zip',
                        help='a file name for the output loadable')

    parser.add_argument('--input_name',
                        type=str,
                        default='input_1',
                        help='name of the input tensor')
    parser.add_argument('--board',
                        type=str,
                        default='NUMAKER_IOT_M487',
                        help='name of the board')
    parser.add_argument('--ram_size', type=str, default=65536, help='ram size')

    args = parser.parse_args()
    compile(args.model, args.samples, args.input_name, args.board,
            args.ram_size, args.output)
