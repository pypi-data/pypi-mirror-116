pip install onnc-bench
onnc-create workbench
cd workbench
onnc-login
./create-infer.py -t vww -o infer1
./build-infer.py -t infer1 -b NUMAKER_IOT_M487
./deploy-infer.py -t infer1 -o ./output
