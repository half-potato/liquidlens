import cv2
from scipy import ndimage
import os, sys
import numpy as np

x_kernel = np.array([[0, -1, 0], [0, 2, 0], [0, -1, 0]])
y_kernel = np.array([[0, 0, 0], [-1, 2, -1], [0, 0, 0]])
mean_kernel = np.ones((5,5))/25

def scale(image):
    mn = np.min(image)
    mx = np.max(image)
    output = np.uint8((image - mn)*255/(mx - mn))
    return output

def modified_laplace(image):
    global x_kernel, y_kernel
    #dx = cv2.filter2D(image.astype(np.float32), -1, x_kernel)
    #dy = cv2.filter2D(image.astype(np.float32), -1, y_kernel)
    dx = ndimage.convolve(image, x_kernel, mode="constant")
    dy = ndimage.convolve(image, y_kernel, mode="constant")
    #return dx + dy
    return np.abs(dx) + np.abs(dy)

# Using gaussian interpolation
# fm = focus measure = modifed laplacian
# d = focus of image taken
# in order of max - step, max, max + step
# Returns:
# depth, s, A # who knows what s and A are? not me
# Ported from: https://www.mathworks.com/matlabcentral/fileexchange/55103-shape-from-focus?focused=5903951&tab=function&requestedDomain=www.mathworks.com
def gaussian_interp(d1, d2, d3, fm1, fm2, fm3):
    c_top = (fm1-fm2 * d2-d3) - (fm2-fm3 * d1-d2)
    c_bot = (d1**2 - d2**2) * (d2-d3) - (d2**2-d3**2)*(d1-d2)
    c = c_top / c_bot
    cv2.imshow("C", c)

    b_top = (fm2-fm3) - c*(d2-d3)*(d2+d3)
    b_bot = (d2-d3)
    b = b_top / b_bot
    cv2.imshow("B", b)

    a = fm1 - b*d1 - c*d1**2
    cv2.imshow("A", a)
    s = np.sqrt(-1/(2*c))
    cv2.imshow("S", s)
    u = b*s**2
    A = np.exp(a + u**2/(2*s**2))
    print(np.nanmean(u))
    print(np.nanstd(u))
    print(np.nanmax(u))
    print(np.nanmin(u))
    return u, s, A

#Mat to index of shape [3, n, n]
# index of the mat along the 3 axis of shape [n,n]
def index_x(mat, inds):
    i, j = np.ogrid[0:mat.shape[1], 0:mat.shape[2]]
    return mat[inds, i, j]

def calc_depth(focuses, focus_measures, step=2):
    max_per_pixel = np.argmax(focus_measures, axis=0)
    minus_one = (max_per_pixel-step) % focus_measures.shape[0]
    plus_one = (max_per_pixel+step) % focus_measures.shape[0]

    d1 = np.choose(minus_one, focuses).astype(np.float32)
    d2 = np.choose(max_per_pixel, focuses).astype(np.float32)
    d3 = np.choose(plus_one, focuses).astype(np.float32)

    fm1 = np.log(index_x(focus_measures, minus_one).astype(np.float32))
    fm2 = np.log(index_x(focus_measures, max_per_pixel).astype(np.float32))
    fm3 = np.log(index_x(focus_measures, plus_one).astype(np.float32))
    cv2.imshow("fm1", fm1)
    cv2.imshow("fm2", fm2)
    cv2.imshow("fm3", fm3)
    u, s, A = gaussian_interp(d1, d2, d3, fm1, fm2, fm3)
    #mx = np.where(u==u.max())
    #mn = np.where(u==u.min())
    #u[mx] = np.max(focuses)
    #u[mn] = np.max(focuses)
    #nan = np.where(np.isnan(u))
    #u[nan] = d2[nan]
    return u * 40

def gray_to_focus(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.GaussianBlur(modified_laplace(gray), (9,9), 0)
    mean = ndimage.convolve(lap, mean_kernel, mode="constant")
    return mean
