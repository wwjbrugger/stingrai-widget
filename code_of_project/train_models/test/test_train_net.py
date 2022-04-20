import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import time

from project_settings import ROOT_PATH

from code_of_project.helper_methods import save_obj_as_txt, save_obj_as_pkl, open_model
from code_of_project.train_models.test.test_args import parse_arguments
from code_of_project.train_models.test.test_prepare_data import prepare_dataset
import pandas as pd

METRICS = [
    keras.metrics.MeanSquaredError(name='mean_squared_error'),
    keras.metrics.MeanSquaredError(name='mean_absolute_error'),
    keras.metrics.MeanSquaredError(name='mean_absolute_percentage_error'),
]


def run():
    args = parse_arguments()
    tf.keras.utils.set_random_seed(0)
    np.random.seed(42)

    train_features, train_labels, val_features, val_labels, test_features, test_labels, \
    feature_columns = prepare_dataset(args)

    model = make_model(args, metrics=METRICS, input_shape=train_features.shape[-1], output_shape=1)
    model.summary()

    model_save_path = construct_save_path(args)

    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=model_save_path / 'logs', histogram_freq=1)
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=model_save_path / 'trained_model/best_model',
        monitor="mean_squared_error", verbose=1,
        save_best_only=True, save_weights_only=False, mode="auto",
        save_freq="epoch")
    train_val_history = model.fit(
        train_features,
        train_labels,
        batch_size=args.batch,
        epochs=args.epochs,
        validation_data=(val_features, val_labels),
        verbose=0,
        callbacks=[tensorboard_callback, checkpoint_callback])

    model = tf.keras.models.load_model(model_save_path / 'trained_model/best_model')

    plot_metrics(train_val_history, model_save_path)

    save_data_and_model_for_future_use(feature_columns, model, model_save_path, test_features, test_labels,
                                       train_features, train_labels, val_features, val_labels, args)

    test_result = model.evaluate(x=test_features, y=test_labels, return_dict=True)
    results_file = model_save_path.parent / 'results_test.txt'
    with open(results_file, 'a') as file1:
        string = f"{model_save_path.name}, " \
                 f"mean_squared_error={test_result['mean_squared_error']:.2f}, " \
                 f"mean_absolute_percentage_error={test_result['mean_absolute_percentage_error']:.2f}, " \
                 f"mean_absolute_error={test_result['mean_absolute_error']:.2f}, " \
                 f"data_file = {args.path_to_dataset.split(sep='/')[-1]}" \
                 f"\n"

        file1.write(string)


def save_data_and_model_for_future_use(feature_columns, model, model_save_path, test_features, test_labels,
                                       train_features, train_labels, val_features, val_labels, args):
    features = pd.concat((train_features, val_features, test_features), axis=0)
    label = pd.concat((train_labels, val_labels, test_labels), axis=0)
    label = label.where(label <= 0.5, 1)
    label = label.where(label > 0.5, 0)
    predictions_data_set = model.predict(features)
    save_obj_as_txt(label.tolist(), model_save_path / 'true_label')
    save_obj_as_pkl(label, model_save_path / 'true_label')
    save_obj_as_txt(predictions_data_set.tolist(), model_save_path / 'prediction')
    save_obj_as_pkl(predictions_data_set, model_save_path / 'prediction')
    save_obj_as_pkl(features, model_save_path / 'scaled_data')
    save_obj_as_txt(feature_columns, model_save_path / 'feature_columns')
    save_obj_as_txt(args.__dict__, model_save_path / 'arguments')


def construct_save_path(args):
    model_save_path = ROOT_PATH / 'models' / 'test_dataset' / \
                      args.experiment_name / time.strftime('%Y:%m:%d-%H:%M:%S')
    return model_save_path


def plot_metrics(history, model_save_path):
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    metrics = ['mean_absolute_error', 'mean_squared_error', 'mean_absolute_percentage_error']
    for n, metric in enumerate(metrics):
        name = metric.replace("_", " ").capitalize()
        plt.subplot(2, 2, n + 1)
        plt.plot(history.epoch, history.history[metric], color=colors[0], label='Train')
        plt.plot(history.epoch, history.history['val_' + metric],
                 color=colors[1], linestyle="--", label='Val')
        plt.xlabel('Epoch')
        plt.ylabel(name)
        if metric == 'loss':
            plt.ylim([0, plt.ylim()[1]])
        elif metric == 'auc':
            plt.ylim([0.8, 1])
        else:
            pass
            # plt.ylim([0, 1])

        plt.legend()
    path_metric_plot = model_save_path / 'metrics.png'
    plt.tight_layout()
    plt.savefig(fname=path_metric_plot)


def make_model(args, input_shape, metrics=None, output_bias=None, output_shape=1):
    if metrics is None:
        metrics = METRICS
    model = keras.Sequential()

    model.add(keras.layers.Dense(args.dense_1_neurons, input_shape=(input_shape,),
                                 activation=args.dense_1_activation, name='dense_1'))
    model.add(keras.layers.Dropout(args.dense_1_dropout_rate, name='dropout_1'))

    if args.use_dense_2:
        model.add(keras.layers.Dense(args.dense_2_neurons, activation=args.dense_2_activation, name='dense_2'))
        model.add(keras.layers.Dropout(args.dense_2_dropout_rate, name='dropout_2'))

    if args.use_dense_3:
        model.add(keras.layers.Dense(args.dense_3_neurons, activation=args.dense_3_activation, name='dense_3'))
        model.add(keras.layers.Dropout(args.dense_3_dropout_rate, name='dropout_3'))

    model.add(keras.layers.Dense(1, input_shape=(input_shape,),
                                 activation='sigmoid', use_bias=False,
                                 name='dense_output')),

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=args.learning_rate),
        loss='mean_absolute_error',
        metrics=metrics)

    return model


if __name__ == '__main__':
    run()
