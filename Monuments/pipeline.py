#---------------------------------------------
# Pipeline
#---------------------------------------------

import os
import pandas as pd
import tensorflow as tf


def path_labels(df):
    # Create path and labels
    path, labels = list(df['path']), list(df['target'])

    # Other formatting
    label_to_index = dict((name, index)
                          for index, name in enumerate(df.target.unique()))
    index_to_label = {v: k for k, v in label_to_index.items()}
    all_image_labels = [label_to_index[l] for l in labels]
    return path, labels, all_image_labels, label_to_index, index_to_label


def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [192, 192])
    image /= 255.0  # normalize to [0,1] range

    return image


def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)


def create_pipe(df, batch_size=32):
    # load data
    all_image_paths, labels, all_image_labels, label_to_index, index_to_label = path_labels(
        df)

    # Preapre prefetch
    AUTOTUNE = tf.data.experimental.AUTOTUNE

    # Create a tensor for the path
    path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)

    # Map to open paths as images
    image_ds = path_ds.map(load_and_preprocess_image,
                           num_parallel_calls=AUTOTUNE)

    # Create a tensor for the labels
    label_ds = tf.data.Dataset.from_tensor_slices(
        tf.cast(all_image_labels, tf.int64))

    # Zip all elements together
    image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))

    # Setting a shuffle buffer size as large as the dataset ensures that the data is
    BATCH_SIZE = batch_size
    image_count = len(labels)
    # completely shuffled.
    ds = image_label_ds.shuffle(buffer_size=image_count)
    ds = ds.repeat()
    ds = ds.batch(BATCH_SIZE)
    # `prefetch` lets the dataset fetch batches in the background while the model is training.
    ds = ds.prefetch(buffer_size=AUTOTUNE)

    return ds, label_to_index, index_to_label


if __name__ == '__main__':
    df = pd.read_csv(f"path_csv.csv")
    ds, label_to_index, index_to_label = create_pipe(df, batch_size=32)

    print(label_to_index)
    print(index_to_label)
    print(type(ds))
    print(ds)
