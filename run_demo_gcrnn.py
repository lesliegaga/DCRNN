import argparse
import numpy as np
import os
import sys
import tensorflow as tf
import yaml

from lib.utils import load_graph_data
from model.gcrnn_supervisor import GCRNNSupervisor


def run_gcrnn(args):
    graph_pkl_filename = 'data/sensor_graph/adj_mx.pkl'
    with open(args.config_filename) as f:
        config = yaml.load(f)
    tf_config = tf.ConfigProto()
    if args.use_cpu_only:
        tf_config = tf.ConfigProto(device_count={'GPU': 0})
    tf_config.gpu_options.allow_growth = True
    _, _, adj_mx = load_graph_data(graph_pkl_filename)
    with tf.Session(config=tf_config) as sess:
        supervisor = GCRNNSupervisor(adj_mx=adj_mx, **config)
        # supervisor.load(sess, config['train']['model_filename'])
        # outputs = supervisor.evaluate(sess)
        # np.savez_compressed(args.output_filename, **outputs)
        # print('Predictions saved as {}.'.format(args.output_filename))


if __name__ == '__main__':
    sys.path.append(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument('--use_cpu_only', default=False, type=str, help='Whether to run tensorflow on cpu.')
    parser.add_argument('--config_filename', default='data/model/gcrnn_pretrained/config.yaml', type=str,
                        help='Config file for pretrained model.')
    parser.add_argument('--output_filename', default='data/gcrnn_predictions.npz')
    args = parser.parse_args()
    run_gcrnn(args)
