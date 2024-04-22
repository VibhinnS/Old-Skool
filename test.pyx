# mandelbrot.pyx
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef mandelbrot(int[:, ::1] output, int width, int height, double xmin, double xmax, double ymin, double ymax, int max_iter):
    cdef int i, j, iter_count
    cdef double x, y, x0, y0, xtemp

    for i in range(width):
        for j in range(height):
            x0 = xmin + (xmax - xmin) * i / width
            y0 = ymin + (ymax - ymin) * j / height
            x = 0.0
            y = 0.0
            iter_count = 0
            while x*x + y*y < 4.0 and iter_count < max_iter:
                xtemp = x*x - y*y + x0
                y = 2*x*y + y0
                x = xtemp
                iter_count += 1

            if iter_count == max_iter:
                output[i, j] = 0
            else:
                output[i, j] = iter_count
