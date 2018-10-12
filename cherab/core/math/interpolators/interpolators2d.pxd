# Copyright 2016-2018 Euratom
# Copyright 2016-2018 United Kingdom Atomic Energy Authority
# Copyright 2016-2018 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

from cherab.core.math.function cimport Function2D
from numpy cimport ndarray, int8_t


cdef class _Interpolate2DBase(Function2D):

    cdef:
        double[::1] _x, _y
        int _extrapolation_type
        double _extrapolation_range

    cdef object _build(self, ndarray x, ndarray y, ndarray f)

    cdef double evaluate(self, double px, double py) except? -1e999

    cdef double _evaluate(self, double px, double py, int i_x, int i_y) except? -1e999

    cdef double _extrapolate(self, double px, double py, int i_x, int i_y, double nearest_px, double nearest_py) except? -1e999

    cdef double _extrapol_linear(self, double px, double py, int i_x, int i_y, double nearest_px, double nearest_py) except? -1e999

    cdef double _extrapol_quadratic(self, double px, double py, int i_x, int i_y, double nearest_px, double nearest_py) except? -1e999


cdef class Interpolate2DLinear(_Interpolate2DBase):

    cdef:
        double[::1] _wx, _wy
        double[:,::1] _wf


cdef class Interpolate2DCubic(_Interpolate2DBase):

    cdef:
        double x_min, x_delta_inv, y_min, y_delta_inv, data_min, data_delta
        double[::1] x_view, x2_view, x3_view
        double[::1] y_view, y2_view, y3_view
        double[:,:] data_view
        double[:,:,::1] coeffs_view
        int8_t[:,::1] calculated_view

    cdef int _calculate_polynomial(self, int i_x, int i_y) except -1

    cdef double _evaluate_polynomial_derivative(self, int i_x, int i_y, double px, double py, int der_x, int der_y)
