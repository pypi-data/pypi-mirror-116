import cupy as cp
import numpy as np

from .._shared.utils import warn
from ..color import rgb2gray, rgba2rgb
from ..util.dtype import dtype_limits, dtype_range

__all__ = ['histogram', 'cumulative_distribution', 'equalize_hist',
           'rescale_intensity', 'adjust_gamma', 'adjust_log', 'adjust_sigmoid']


DTYPE_RANGE = dtype_range.copy()
DTYPE_RANGE.update((d.__name__, limits) for d, limits in dtype_range.items())
DTYPE_RANGE.update({'uint10': (0, 2 ** 10 - 1),
                    'uint12': (0, 2 ** 12 - 1),
                    'uint14': (0, 2 ** 14 - 1),
                    'bool': dtype_range[bool],
                    'float': dtype_range[np.float64]})


def _offset_array(arr, low_boundary, high_boundary):
    """Offset the array to get the lowest value at 0 if negative."""
    if low_boundary < 0:
        offset = low_boundary
        dyn_range = high_boundary - low_boundary
        # get smallest dtype that can hold both minimum and offset maximum
        offset_dtype = np.promote_types(np.min_scalar_type(dyn_range),
                                        np.min_scalar_type(low_boundary))
        if arr.dtype != offset_dtype:
            # prevent overflow errors when offsetting
            arr = arr.astype(offset_dtype)
        arr = arr - offset
    else:
        offset = 0
    return arr, offset


def _bincount_histogram(image, source_range):
    """
    Efficient histogram calculation for an image of integers.

    This function is significantly more efficient than cupy.histogram but
    works only on images of integers. It is based on cupy.bincount.

    Parameters
    ----------
    image : array
        Input image.
    source_range : string
        'image' determines the range from the input image.
        'dtype' determines the range from the expected range of the images
        of that data type.

    Returns
    -------
    hist : array
        The values of the histogram.
    bin_centers : array
        The values at the center of the bins.
    """
    if source_range not in ['image', 'dtype']:
        raise ValueError('Incorrect value for `source_range` argument: '
                         f'{source_range}')
    if source_range == 'image':
        image_min = int(image.min().astype(np.int64))
        image_max = int(image.max().astype(np.int64))
    elif source_range == 'dtype':
        image_min, image_max = dtype_limits(image, clip_negative=False)
    image, offset = _offset_array(image, image_min, image_max)
    hist = cp.bincount(image.ravel(), minlength=image_max - image_min + 1)
    bin_centers = cp.arange(image_min, image_max + 1)
    if source_range == 'image':
        idx = max(image_min, 0)
        hist = hist[idx:]
    return hist, bin_centers


def histogram(image, nbins=256, source_range='image', normalize=False):
    """Return histogram of image.

    Unlike `numpy.histogram`, this function returns the centers of bins and
    does not rebin integer arrays. For integer arrays, each integer value has
    its own bin, which improves speed and intensity-resolution.

    The histogram is computed on the flattened image: for color images, the
    function should be used separately on each channel to obtain a histogram
    for each color channel.

    Parameters
    ----------
    image : array
        Input image.
    nbins : int, optional
        Number of bins used to calculate histogram. This value is ignored for
        integer arrays.
    source_range : string, optional
        'image' (default) determines the range from the input image.
        'dtype' determines the range from the expected range of the images
        of that data type.
    normalize : bool, optional
        If True, normalize the histogram by the sum of its values.

    Returns
    -------
    hist : array
        The values of the histogram.
    bin_centers : array
        The values at the center of the bins.

    See Also
    --------
    cumulative_distribution

    Examples
    --------
    >>> import cupy as cp
    >>> from skimage import data
    >>> from cucim.skimage import exposure, img_as_float
    >>> image = img_as_float(cp.array(data.camera()))
    >>> cp.histogram(image, bins=2)
    (array([ 93585, 168559]), array([0. , 0.5, 1. ]))
    >>> exposure.histogram(image, nbins=2)
    (array([ 93585, 168559]), array([0.25, 0.75]))
    """
    sh = image.shape
    if len(sh) == 3 and sh[-1] < 4:
        warn("This might be a color image. The histogram will be "
             "computed on the flattened image. You can instead "
             "apply this function to each color channel.")

    image = image.flatten()
    # For integer types, histogramming with bincount is more efficient.
    if np.issubdtype(image.dtype, np.integer):
        hist, bin_centers = _bincount_histogram(image, source_range)
    else:
        if source_range == 'image':
            hist_range = None
        elif source_range == 'dtype':
            hist_range = dtype_limits(image, clip_negative=False)
        else:
            ValueError('Wrong value for the `source_range` argument')
        hist, bin_edges = cp.histogram(image, bins=nbins, range=hist_range)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.

    if normalize:
        hist = hist / cp.sum(hist)
    return hist, bin_centers


def cumulative_distribution(image, nbins=256):
    """Return cumulative distribution function (cdf) for the given image.

    Parameters
    ----------
    image : array
        Image array.
    nbins : int, optional
        Number of bins for image histogram.

    Returns
    -------
    img_cdf : array
        Values of cumulative distribution function.
    bin_centers : array
        Centers of bins.

    See Also
    --------
    histogram

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Cumulative_distribution_function

    Examples
    --------
    >>> import cupy as cp
    >>> from skimage import data
    >>> from cucim.skimage import exposure, img_as_float
    >>> image = img_as_float(cp.array(data.camera()))
    >>> hi = exposure.histogram(image)
    >>> cdf = exposure.cumulative_distribution(image)
    >>> cp.alltrue(cdf[0] == cp.cumsum(hi[0])/float(image.size))
    True
    """
    hist, bin_centers = histogram(image, nbins)
    img_cdf = hist.cumsum()
    img_cdf = img_cdf / float(img_cdf[-1])
    return img_cdf, bin_centers


def equalize_hist(image, nbins=256, mask=None):
    """Return image after histogram equalization.

    Parameters
    ----------
    image : array
        Image array.
    nbins : int, optional
        Number of bins for image histogram. Note: this argument is
        ignored for integer images, for which each integer is its own
        bin.
    mask: ndarray of bools or 0s and 1s, optional
        Array of same shape as `image`. Only points at which mask == True
        are used for the equalization, which is applied to the whole image.

    Returns
    -------
    out : float array
        Image array after histogram equalization.

    Notes
    -----
    This function is adapted from [1]_ with the author's permission.

    References
    ----------
    .. [1] http://www.janeriksolem.net/histogram-equalization-with-python-and.html
    .. [2] https://en.wikipedia.org/wiki/Histogram_equalization

    """  # noqa
    if mask is not None:
        mask = mask.astype(bool, copy=False)
        cdf, bin_centers = cumulative_distribution(image[mask], nbins)
    else:
        cdf, bin_centers = cumulative_distribution(image, nbins)
    out = cp.interp(image.ravel(), bin_centers, cdf)
    return out.reshape(image.shape)


def intensity_range(image, range_values="image", clip_negative=False):
    """Return image intensity range (min, max) based on desired value type.

    Parameters
    ----------
    image : array
        Input image.
    range_values : str or 2-tuple, optional
        The image intensity range is configured by this parameter.
        The possible values for this parameter are enumerated below.

        'image'
            Return image min/max as the range.
        'dtype'
            Return min/max of the image's dtype as the range.
        dtype-name
            Return intensity range based on desired `dtype`. Must be valid key
            in `DTYPE_RANGE`. Note: `image` is ignored for this range type.
        2-tuple
            Return `range_values` as min/max intensities. Note that there's no
            reason to use this function if you just want to specify the
            intensity range explicitly. This option is included for functions
            that use `intensity_range` to support all desired range types.

    clip_negative : bool, optional
        If True, clip the negative range (i.e. return 0 for min intensity)
        even if the image dtype allows negative values.

    Returns
    -------
    i_range : tuple
        A 2-tuple where the first element is the minimum and the second is the
        maximum.
    """
    if range_values == 'dtype':
        range_values = image.dtype.type

    if range_values == 'image':
        i_min = image.min().item()
        i_max = image.max().item()
    elif range_values in DTYPE_RANGE:
        i_min, i_max = DTYPE_RANGE[range_values]
        if clip_negative:
            i_min = 0
    else:
        i_min, i_max = range_values
    return i_min, i_max


def _output_dtype(dtype_or_range):
    """Determine the output dtype for rescale_intensity.

    The dtype is determined according to the following rules:
    - if ``dtype_or_range`` is a dtype, that is the output dtype.
    - if ``dtype_or_range`` is a dtype string, that is the dtype used, unless
      it is not a NumPy data type (e.g. 'uint12' for 12-bit unsigned integers),
      in which case the data type that can contain it will be used
      (e.g. uint16 in this case).
    - if ``dtype_or_range`` is a pair of values, the output data type will be
      float.

    Parameters
    ----------
    dtype_or_range : type, string, or 2-tuple of int/float
        The desired range for the output, expressed as either a NumPy dtype or
        as a (min, max) pair of numbers.

    Returns
    -------
    out_dtype : type
        The data type appropriate for the desired output.
    """
    if type(dtype_or_range) in [list, tuple, np.ndarray]:
        # pair of values: always return float.
        return float
    if type(dtype_or_range) == type:
        # already a type: return it
        return dtype_or_range
    if dtype_or_range in DTYPE_RANGE:
        # string key in DTYPE_RANGE dictionary
        try:
            # if it's a canonical numpy dtype, convert
            return np.dtype(dtype_or_range).type
        except TypeError:  # uint10, uint12, uint14
            # otherwise, return uint16
            return np.uint16
    else:
        raise ValueError(
            'Incorrect value for out_range, should be a valid image data '
            f'type or a pair of values, got {dtype_or_range}.'
        )


def rescale_intensity(image, in_range="image", out_range="dtype"):
    """Return image after stretching or shrinking its intensity levels.

    The desired intensity range of the input and output, `in_range` and
    `out_range` respectively, are used to stretch or shrink the intensity range
    of the input image. See examples below.

    Parameters
    ----------
    image : array
        Image array.
    in_range, out_range : str or 2-tuple, optional
        Min and max intensity values of input and output image.
        The possible values for this parameter are enumerated below.

        'image'
            Use image min/max as the intensity range.
        'dtype'
            Use min/max of the image's dtype as the intensity range.
        dtype-name
            Use intensity range based on desired `dtype`. Must be valid key
            in `DTYPE_RANGE`.
        2-tuple
            Use `range_values` as explicit min/max intensities.

    Returns
    -------
    out : array
        Image array after rescaling its intensity. This image is the same dtype
        as the input image.

    Notes
    -----
    .. versionchanged:: 0.17
        The dtype of the output array has changed to match the output dtype, or
        float if the output range is specified by a pair of floats.

    See Also
    --------
    equalize_hist

    Examples
    --------
    By default, the min/max intensities of the input image are stretched to
    the limits allowed by the image's dtype, since `in_range` defaults to
    'image' and `out_range` defaults to 'dtype':

    >>> image = cp.array([51, 102, 153], dtype=np.uint8)
    >>> rescale_intensity(image)
    array([  0, 127, 255], dtype=uint8)

    It's easy to accidentally convert an image dtype from uint8 to float:

    >>> 1.0 * image
    array([ 51., 102., 153.])

    Use `rescale_intensity` to rescale to the proper range for float dtypes:

    >>> image_float = 1.0 * image
    >>> rescale_intensity(image_float)
    array([0. , 0.5, 1. ])

    To maintain the low contrast of the original, use the `in_range` parameter:

    >>> rescale_intensity(image_float, in_range=(0, 255))
    array([0.2, 0.4, 0.6])

    If the min/max value of `in_range` is more/less than the min/max image
    intensity, then the intensity levels are clipped:

    >>> rescale_intensity(image_float, in_range=(0, 102))
    array([0.5, 1. , 1. ])

    If you have an image with signed integers but want to rescale the image to
    just the positive range, use the `out_range` parameter. In that case, the
    output dtype will be float:

    >>> image = cp.asarray([-10, 0, 10], dtype=np.int8)
    >>> rescale_intensity(image, out_range=(0, 127))
    array([  0. ,  63.5, 127. ])

    To get the desired range with a specific dtype, use ``.astype()``:

    >>> rescale_intensity(image, out_range=(0, 127)).astype(np.int8)
    array([  0,  63, 127], dtype=int8)

    If the input image is constant, the output will be clipped directly to the
    output range:
    >>> image = cp.asarray([130, 130, 130], dtype=np.int32)
    >>> rescale_intensity(image, out_range=(0, 127)).astype(np.int32)
    array([127, 127, 127], dtype=int32)
    """
    if out_range in ['dtype', 'image']:
        out_dtype = _output_dtype(image.dtype.type)
    else:
        out_dtype = _output_dtype(out_range)

    imin, imax = map(float, intensity_range(image, in_range))
    omin, omax = map(float, intensity_range(image, out_range,
                                            clip_negative=(imin >= 0)))

    if np.any(np.isnan([imin, imax, omin, omax])):
        warn(
            "One or more intensity levels are NaN. Rescaling will broadcast "
            "NaN to the full image. Provide intensity levels yourself to "
            "avoid this. E.g. with np.nanmin(image), np.nanmax(image).",
            stacklevel=2
        )

    image = cp.clip(image, imin, imax)

    if imin != imax:
        image = (image - imin) / (imax - imin)
        return cp.asarray(image * (omax - omin) + omin, dtype=out_dtype)
    else:
        return cp.clip(image, omin, omax).astype(out_dtype, copy=False)


def _assert_non_negative(image):

    if cp.any(image < 0):  # synchronize!
        raise ValueError('Image Correction methods work correctly only on '
                         'images with non-negative values. Use '
                         'skimage.exposure.rescale_intensity.')


def _adjust_gamma_u8(image, gamma, gain):
    """LUT based implmentation of gamma adjustement."""
    lut = (255 * gain * (np.linspace(0, 1, 256) ** gamma)).astype("uint8")
    lut = cp.asarray(lut)
    return lut[image]


def adjust_gamma(image, gamma=1, gain=1):
    """Performs Gamma Correction on the input image.

    Also known as Power Law Transform.
    This function transforms the input image pixelwise according to the
    equation ``O = I**gamma`` after scaling each pixel to the range 0 to 1.

    Parameters
    ----------
    image : ndarray
        Input image.
    gamma : float, optional
        Non negative real number. Default value is 1.
    gain : float, optional
        The constant multiplier. Default value is 1.

    Returns
    -------
    out : ndarray
        Gamma corrected output image.

    See Also
    --------
    adjust_log

    Notes
    -----
    For gamma greater than 1, the histogram will shift towards left and
    the output image will be darker than the input image.

    For gamma less than 1, the histogram will shift towards right and
    the output image will be brighter than the input image.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Gamma_correction

    Examples
    --------
    >>> from skimage import data
    >>> from cucim.skimage import exposure, img_as_float
    >>> image = img_as_float(cp.array(data.moon()))
    >>> gamma_corrected = exposure.adjust_gamma(image, 2)
    >>> # Output is darker for gamma > 1
    >>> image.mean() > gamma_corrected.mean()
    True
    """
    if gamma < 0:
        raise ValueError("Gamma should be a non-negative real number.")

    dtype = image.dtype.type

    if dtype is cp.uint8:
        out = _adjust_gamma_u8(image, gamma, gain)
    else:
        _assert_non_negative(image)

        scale = float(dtype_limits(image, True)[1]
                      - dtype_limits(image, True)[0])

        out = (((image / scale) ** gamma) * scale * gain).astype(dtype)

    return out


def adjust_log(image, gain=1, inv=False):
    """Performs Logarithmic correction on the input image.

    This function transforms the input image pixelwise according to the
    equation ``O = gain*log(1 + I)`` after scaling each pixel to the range
    0 to 1.

    For inverse logarithmic correction, the equation is
    ``O = gain*(2**I - 1)``.

    Parameters
    ----------
    image : ndarray
        Input image.
    gain : float, optional
        The constant multiplier. Default value is 1.
    inv : float, optional
        If True, it performs inverse logarithmic correction,
        else correction will be logarithmic. Defaults to False.

    Returns
    -------
    out : ndarray
        Logarithm corrected output image.

    See Also
    --------
    adjust_gamma

    References
    ----------
    .. [1] http://www.ece.ucsb.edu/Faculty/Manjunath/courses/ece178W03/EnhancePart1.pdf

    """  # noqa
    _assert_non_negative(image)
    dtype = image.dtype.type
    scale = float(dtype_limits(image, True)[1] - dtype_limits(image, True)[0])

    if inv:
        out = (2 ** (image / scale) - 1) * scale * gain
        return out.astype(dtype, copy=False)

    out = cp.log2(1 + image / scale) * scale * gain
    return out.astype(dtype, copy=False)


def adjust_sigmoid(image, cutoff=0.5, gain=10, inv=False):
    """Performs Sigmoid Correction on the input image.

    Also known as Contrast Adjustment.
    This function transforms the input image pixelwise according to the
    equation ``O = 1/(1 + exp*(gain*(cutoff - I)))`` after scaling each pixel
    to the range 0 to 1.

    Parameters
    ----------
    image : ndarray
        Input image.
    cutoff : float, optional
        Cutoff of the sigmoid function that shifts the characteristic curve
        in horizontal direction. Default value is 0.5.
    gain : float, optional
        The constant multiplier in exponential's power of sigmoid function.
        Default value is 10.
    inv : bool, optional
        If True, returns the negative sigmoid correction. Defaults to False.

    Returns
    -------
    out : ndarray
        Sigmoid corrected output image.

    See Also
    --------
    adjust_gamma

    References
    ----------
    .. [1] Gustav J. Braun, "Image Lightness Rescaling Using Sigmoidal Contrast
           Enhancement Functions",
           http://www.cis.rit.edu/fairchild/PDFs/PAP07.pdf

    """
    _assert_non_negative(image)
    dtype = image.dtype.type
    scale = float(dtype_limits(image, True)[1] - dtype_limits(image, True)[0])

    if inv:
        out = (1 - 1 / (1 + cp.exp(gain * (cutoff - image / scale)))) * scale
        return out.astype(dtype, copy=False)

    out = (1 / (1 + cp.exp(gain * (cutoff - image / scale)))) * scale
    return out.astype(dtype, copy=False)


def is_low_contrast(image, fraction_threshold=0.05, lower_percentile=1,
                    upper_percentile=99, method='linear'):
    """Determine if an image is low contrast.

    Parameters
    ----------
    image : array-like
        The image under test.
    fraction_threshold : float, optional
        The low contrast fraction threshold. An image is considered low-
        contrast when its range of brightness spans less than this
        fraction of its data type's full range. [1]_
    lower_percentile : float, optional
        Disregard values below this percentile when computing image contrast.
    upper_percentile : float, optional
        Disregard values above this percentile when computing image contrast.
    method : str, optional
        The contrast determination method.  Right now the only available
        option is "linear".

    Returns
    -------
    out : bool
        True when the image is determined to be low contrast.

    References
    ----------
    .. [1] https://scikit-image.org/docs/dev/user_guide/data_types.html

    Examples
    --------
    >>> import cupy as cp
    >>> image = cp.linspace(0, 0.04, 100)
    >>> is_low_contrast(image)
    True
    >>> image[-1] = 1
    >>> is_low_contrast(image)
    True
    >>> is_low_contrast(image, upper_percentile=100)
    False
    """
    if image.ndim == 3:
        if image.shape[2] == 4:
            image = rgba2rgb(image)
        if image.shape[2] == 3:
            image = rgb2gray(image)

    dlimits = dtype_limits(image, clip_negative=False)
    limits = cp.percentile(image, [lower_percentile, upper_percentile])
    ratio = (limits[1] - limits[0]) / (dlimits[1] - dlimits[0])

    return ratio < fraction_threshold
