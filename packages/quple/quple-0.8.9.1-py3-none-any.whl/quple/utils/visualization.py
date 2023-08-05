from typing import Optional, Dict

import matplotlib.pyplot as plt

def visualize_images(images:"numpy.ndarray", columns:int=8, subplots_options:Optional[Dict]=None):
    """Visualize a set of 2D images in a grid
    
    Arguments:
        images: numpy.ndarray
            A 3D numpy array representing batches of images of shape (batchsize, rows, cols)
        colunms: int
            Number of coumns in the grid
        subplots_options: Optional[Dict]
            A dictionary containing subplots options
    Returns:
        matplotlib.pyplot object
    """
    plt.clf()
    size = images.shape[0]
    rows = ( size // columns ) + 1
    fig = plt.figure(figsize=(20, rows*3))
    for i in range(images.shape[0]):
        ax = fig.add_subplot(rows, columns, i+1)
        ax.imshow(images[i])
    if subplots_options is not None:
        plt.subplots_adjust(**subplots_options)
    return plt