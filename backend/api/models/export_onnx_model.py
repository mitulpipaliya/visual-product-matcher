# this script was run on google colab to avoid dependency issues

import tensorflow as tf
import tf2onnx

base_model = tf.keras.applications.MobileNetV3Small(
    weights="imagenet", 
    include_top=False,    
    pooling="avg"        
)

model = tf.keras.Model(inputs=base_model.input, outputs=base_model.output)
spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="input"),)
output_path = "mobilenetv3small.onnx"
model_proto, _ = tf2onnx.convert.from_keras(
    model, 
    input_signature=spec, 
    output_path=output_path,
    opset=17
)
print("Done mobilenetv3small.onnx")