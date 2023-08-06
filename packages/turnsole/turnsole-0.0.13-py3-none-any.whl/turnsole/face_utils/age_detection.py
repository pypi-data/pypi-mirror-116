# -*- coding: utf-8 -*-
# @Author        : lk
# @Email         : 9428.al@gmail.com
# @Create Date   : 2021-08-11 17:10:16
# @Last Modified : 2021-08-12 13:29:28
# @Description   : 

import os
import tensorflow as tf

class AGE_DETECTION:
    def __init__(self, model_path):
        self.age_map = {
                        0: '0-2',
                        1: '4-6',
                        2: '8-13',
                        3: '15-20',
                        4: '25-32',
                        5: '38-43',
                        6: '48-53',
                        7: '60+'
                    }

        self.model = tf.keras.models.load_model(filepath=model_path,
                                                compile=False)
        self.inference_model = self.build_inference_model()

    def build_inference_model(self):
        image = self.model.input
        x = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        predictions = self.model(x, training=False)
        index = tf.argmax(predictions, axis=-1)
        inference_model = tf.keras.Model(inputs=image, outputs=index)
        return inference_model

    def predict_batch(self, images):
        # inputs images should be images list, whatever your shape
        # return a list of prediction results
        images = tf.stack([tf.image.resize(image, [96, 96]) for image in images], axis=0)
        preds = self.inference_model.predict(images)
        outputs = [self.age_map[pred] for pred in preds]
        return outputs

if __name__ == '__main__':
    from turnsole import paths

    age_det = AGE_DETECTION(model_path='./ckpt/model.h5')

    data_dir = '/home/lk/Project/Face_Age_Gender/data/Emotion/emotion/010003_female_yellow_22'

    all_data = paths.list_images(data_dir)

    for image_path in all_data:
        print(image_path)

        image = tf.io.read_file(image_path)
        image = tf.io.decode_jpeg(image)

        x = age_det.predict_batch([image])

        print(x)

