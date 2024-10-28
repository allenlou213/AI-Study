import tensorflow as tf
from tensorflow.keras import layers

# 定义模型
model = tf.keras.Sequential()

# 添加输入层，假设输入数据的维度是 10
model.add(layers.Dense(32, activation='relu', input_shape=(10,)))

# 添加隐藏层
model.add(layers.Dense(32, activation='relu'))

# 添加输出层，假设输出数据的维度是 1
model.add(layers.Dense(1))

# 编译模型
model.compile(optimizer='adam', loss='mean_squared_error')

# 打印模型的概要信息
model.summary()