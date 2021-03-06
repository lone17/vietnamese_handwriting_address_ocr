from keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from models import *

cb_list = []

tb = TensorBoard(log_dir='/logs', write_graph=True, write_images=True)
cb_list.append(tb)

es = EarlyStopping(monitor='loss', patience=4, mode='min', verbose=1)
cb_list.append(es)
cp = ModelCheckpoint(filepath='checkpoints/{val_loss:.2f}.crnn',
                     monitor='val_loss', verbose=1, mode='min', save_best_only=True)
cb_list.append(cp)

model = crnn()
gen = DataGenerator('X_2', 'y_2', desample_factor['crnn'], 16)
import tensorflow as tf
with tf.device('/gpu:0'):
    model.fit_generator(generator=gen.next_train(),
                        steps_per_epoch=gen.train_steps,
                        validation_data=gen.next_val(),
                        validation_steps=gen.val_steps,
                        epochs=100,
                        callbacks=cb_list,
                        verbose=1,
                        )
