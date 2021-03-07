import os
import sys
import numpy as np
import h5py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


def fetch_modelnet40():
    # Download dataset for point cloud classification
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    if not os.path.exists(DATA_DIR):
        print('ModelNet40 Dataset does not exist. Retrieving files...')
        os.mkdir(DATA_DIR)
    if not os.path.exists(os.path.join(DATA_DIR, 'modelnet40_ply_hdf5_2048')):
        www = 'https://shapenet.cs.stanford.edu/media/modelnet40_ply_hdf5_2048.zip'
        zipfile = os.path.basename(www)
        print('Starting download...')
        os.system('wget %s --no-check-certificate; unzip %s' % (www, zipfile))
        os.system('mv %s %s' % (zipfile[:-4], DATA_DIR))
        print('Finished downloading. Cleaning up files..')
        os.system('rm %s' % (zipfile))
    print('ModelNet40 is ready.')


def shuffle_data(data, labels):
    """
    Shuffle data and training labels
    :param data: B,N,... numpy array
    :param labels: B,... numpy array
    :return: Shuffled data, label and indices
    """
    idx = np.arange(len(labels))
    np.random.shuffle(idx)
    return data[idx, ...], labels[idx], idx


def rotate_point_cloud(batch_data):
    """
    Introduce random rotation to point clouds in batch.
    :param batch_data: B,N,3 numpy array. Batch of 3D point clouds
    :return: B,N,3 numpy array. Batch of original point clouds but random rotations are applied
    """
    rotated_data = np.zeros_like(batch_data, dtype=np.float32)
    for k in range(batch_data.shape[0]):
        theta = np.random.uniform() * 2 * np.pi
        cosine = np.cos(theta)
        sine = np.sin(theta)
        rotation_matrix = np.array([
            [cosine, 0, sine],
            [0, 1, 0],
            [-sine, 0, cosine]
        ])
        original_pc = batch_data[k, ...]   # get k-th point cloud
        rotated_data[k, ...] = np.dot(original_pc.reshape(-1, 3), rotation_matrix)
    return rotated_data


def rotate_point_cloud_by_angle(batch_data, theta):
    """
    Introduce rotation to point clouds in batch.
    :param batch_data: B,N,3 numpy array. Batch of 3D point clouds
    :param theta: Floating point number. Rotation angle used for rotating point clouds
    :return: B,N,3 numpy array. Batch of original point clouds but random rotations are applied
    """
    rotated_data = np.zeros_like(batch_data, dtype=np.float32)
    for k in range(batch_data.shape[0]):
        cosine = np.cos(theta)
        sine = np.sin(theta)
        rotation_matrix = np.array([
            [cosine, 0, sine],
            [0, 1, 0],
            [-sine, 0, cosine]
        ])
        original_pc = batch_data[k, ...]  # get k-th point cloud
        rotated_data[k, ...] = np.dot(original_pc.reshape(-1, 3), rotation_matrix)
    return rotated_data