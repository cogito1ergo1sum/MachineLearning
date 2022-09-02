import numpy as np

def get_random_centroids(X, k):

    '''
    Each centroid is a point in RGB space (color) in the image. 
    This function should uniformly pick `k` centroids from the dataset.
    Input: a single image of shape `(num_pixels, 3)` and `k`, the number of centroids. 
    Notice we are flattening the image to a two dimentional array.
    Output: Randomly chosen centroids of shape `(k,3)` as a numpy array. 
    '''
    
    centroids = []
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    centroids = X[np.random.choice(X.shape[0], k, replace=False), :]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    # make sure you return a numpy array
    return np.asarray(centroids).astype(np.float) 



def lp_distance(X, centroids, p=2):

    '''
    Inputs: 
    A single image of shape (num_pixels, 3)
    The centroids (k, 3)
    The distance parameter p

    output: numpy array of shape `(k, num_pixels)` thats holds the distances of 
    all points in RGB space from all centroids
    '''
    distances = []
    k = len(centroids)
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    X_repeat = np.repeat(np.expand_dims(X, 0), k, axis=0).astype(float)
    centroids = np.expand_dims(centroids, 1)
    distances = np.sum(np.abs(X_repeat - centroids) ** p, axis=2) ** (1 / p)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return distances

def kmeans(X, k, p ,max_iter=100):
    """
    Inputs:
    - X: a single image of shape (num_pixels, 3).
    - k: number of centroids.
    - p: the parameter governing the distance measure.
    - max_iter: the maximum number of iterations to perform.

    Outputs:
    - The calculated centroids as a numpy array.
    - The final assignment of all RGB points to the closest centroids as a numpy array.
    """
    classes = []
    centroids = get_random_centroids(X, k)
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    cents_new = np.zeros(centroids.shape)
    for i in range(max_iter):
        dist = lp_distance(X, centroids, p) 
        classes = np.argmin(dist, axis=0)  
        cents_new = np.array([X[classes == j].mean(axis=0) for j in range(k)])

        if np.array_equal(centroids, cents_new):
            return centroids, classes
        centroids = cents_new.copy()
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return centroids, classes

def kmeans_pp(X, k, p ,max_iter=100):
    """
    Your implenentation of the kmeans++ algorithm.
    Inputs:
    - X: a single image of shape (num_pixels, 3).
    - k: number of centroids.
    - p: the parameter governing the distance measure.
    - max_iter: the maximum number of iterations to perform.

    Outputs:
    - The calculated centroids as a numpy array.
    - The final assignment of all RGB points to the closest centroids as a numpy array.
    """
    classes = None
    centroids = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    centroids = np.array([])
    X_copy = X.copy()

    random_index = np.random.randint(0, len(X_copy))
    centroids = np.expand_dims(X_copy[random_index], axis=0)  
    np.delete(X_copy, random_index)

    for k in range(k):
        
        dist = lp_distance(X, centroids, p)
        min_dist = np.min(dist, axis=0)
        sq_dist = np.sum(min_dist ** 2)
        prob_dist = min_dist ** 2 / sq_dist
        
        new_centroid_ind = np.random.choice(np.arange(0, X_copy.shape[0]), size=1, p=prob_dist)
        new_centroid = X_copy[new_centroid_ind]
        centroids = np.append(centroids, new_centroid, axis=0)
        np.delete(X_copy, new_centroid_ind)

    for i in range(max_iter):
        final_centroids = centroids
        dist = lp_distance(X, centroids, p)
        classes = np.argmin(dist, axis=0)
        centroids = np.array([np.mean(X[np.where(classes == centroid_index)], axis=0) for centroid_index in range(len(centroids))])
        
        if np.allclose(final_centroids, centroids):
            break

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return centroids, classes
