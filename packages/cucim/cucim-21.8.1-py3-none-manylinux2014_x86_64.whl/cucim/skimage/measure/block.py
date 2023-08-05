import cupy as cp

from ..util import view_as_blocks


def block_reduce(image, block_size, func=cp.sum, cval=0, func_kwargs=None):
    """Downsample image by applying function `func` to local blocks.

    This function is useful for max and mean pooling, for example.

    Parameters
    ----------
    image : ndarray
        N-dimensional input image.
    block_size : array_like
        Array containing down-sampling integer factor along each axis.
    func : callable
        Function object which is used to calculate the return value for each
        local block. This function must implement an ``axis`` parameter.
        Primary functions are ``numpy.sum``, ``numpy.min``, ``numpy.max``,
        ``numpy.mean`` and ``numpy.median``.  See also `func_kwargs`.
    cval : float
        Constant padding value if image is not perfectly divisible by the
        block size.
    func_kwargs : dict
        Keyword arguments passed to `func`. Notably useful for passing dtype
        argument to ``np.mean``. Takes dictionary of inputs, e.g.:
        ``func_kwargs={'dtype': np.float16})``.

    Returns
    -------
    image : ndarray
        Down-sampled image with same number of dimensions as input image.

    Examples
    --------
    >>> import cupy as cp
    >>> from skimage.measure import block_reduce
    >>> image = cp.arange(3*3*4).reshape(3, 3, 4)
    >>> image # doctest: +NORMALIZE_WHITESPACE
    array([[[ 0,  1,  2,  3],
            [ 4,  5,  6,  7],
            [ 8,  9, 10, 11]],
           [[12, 13, 14, 15],
            [16, 17, 18, 19],
            [20, 21, 22, 23]],
           [[24, 25, 26, 27],
            [28, 29, 30, 31],
            [32, 33, 34, 35]]])
    >>> block_reduce(image, block_size=(3, 3, 1), func=cp.mean)
    array([[[16., 17., 18., 19.]]])
    >>> image_max1 = block_reduce(image, block_size=(1, 3, 4), func=cp.max)
    >>> image_max1 # doctest: +NORMALIZE_WHITESPACE
    array([[[11]],
           [[23]],
           [[35]]])
    >>> image_max2 = block_reduce(image, block_size=(3, 1, 4), func=cp.max)
    >>> image_max2 # doctest: +NORMALIZE_WHITESPACE
    array([[[27],
            [31],
            [35]]])
    """

    if len(block_size) != image.ndim:
        raise ValueError("`block_size` must have the same length "
                         "as `image.shape`.")

    if func_kwargs is None:
        func_kwargs = {}

    pad_width = []
    for i in range(len(block_size)):
        if block_size[i] < 1:
            raise ValueError("Down-sampling factors must be >= 1. Use "
                             "`skimage.transform.resize` to up-sample an "
                             "image.")
        if image.shape[i] % block_size[i] != 0:
            after_width = block_size[i] - (image.shape[i] % block_size[i])
        else:
            after_width = 0
        pad_width.append((0, after_width))

    image = cp.pad(image, pad_width=pad_width, mode='constant',
                   constant_values=cval)

    blocked = view_as_blocks(image, block_size)

    return func(blocked, axis=tuple(range(image.ndim, blocked.ndim)),
                **func_kwargs)
