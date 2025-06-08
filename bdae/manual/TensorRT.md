First of all, Install TensorRT from NVIDIA according to your Graphic Card.
I installed, TensorRT-8.5.1.7 

```
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov5su.pt")

# Export the model to TensorRT format
model.export(format="engine")  # creates 'yolov8n.engine'
```

Detect (Infer)
```
from ultralytics import YOLO
tensorrt_model = YOLO("yolov5s.engine")

# Run inference
results = tensorrt_model("https://ultralytics.com/images/bus.jpg", task='detect')
```

### From Command
You must adjust the same versions...
```
trtexec --onnx=yolov5su.onnx --saveEngine=yolov5s.engine
```
you can infer the above engine.
