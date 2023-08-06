import tensorflow as tf
import numpy as np
from onnc.bench import launch

# load and split datasets
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# normalize dataset
x_train, x_test = x_train / 255.0, x_test / 255.0


x_train = np.expand_dims(x_train, axis=1)
x_test = np.expand_dims(x_test, axis=1)

# define model architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(1, 28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])

# define loss function
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# train model
model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])
model.fit(x_train, y_train, epochs=1)

# evaluate model
model.evaluate(x_test, y_test, verbose=2)


# Setup your ONNC API key
api_key = "Your-API-Key"
print(api_key)
# Instantiate a workspace for deploying model for device `M487`
workspace = launch(api_key, 'NUMAKER_IOT_M487')

# Quantize model to improve performance and reduce memory footprint.
# Here we need quantization dataset, using validation dataset
# is surfficent.
workspace.quantize(x_test)

# Compile the model and get the compilation results
report = workspace.compile(model, "input_1", "dense_1")["report"]

# Save the compiled model
workspace.save('./output')

# Release disk space in cloud
workspace.close()

print(report)
"""
{'ram': 2490, 'rom': 101970}

The report shows we need:
    2,490 bytes of SRAM
  101,970 bytes of ROM
to run this model on a CortexM device.
"""
