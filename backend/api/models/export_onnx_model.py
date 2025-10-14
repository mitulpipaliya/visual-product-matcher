# this script was run on google colab to avoid dependency issues

import tensorflow as tf
import tf2onnx

base_model = tf.keras.applications.MobileNetV3Small(weights="imagenet", include_top=False, pooling="avg")
x = tf.keras.layers.Dense(512, activation=None, name="embedding_layer")(base_model.output)
model = tf.keras.Model(inputs=base_model.input, outputs=x)

spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="input"),)
model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, output_path="mobilenetv3small_512.onnx")

print("saved mobilenetv3small_512.onnx")
