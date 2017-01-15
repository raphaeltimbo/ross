import pytest
from LaviRot.elements import *
from LaviRot.rotor import *
from LaviRot.results import MAC_modes
import numpy as np
from numpy.testing import assert_almost_equal, assert_allclose


@pytest.fixture
def rotor1():
    #  Rotor without damping with 2 shaft elements - no disks and no bearings
    le_ = 0.25
    i_d_ = 0
    o_d_ = 0.05
    E_ = 211e9
    G_ = 81.2e9
    rho_ = 7810

    tim0 = ShaftElement(0, le_, i_d_, o_d_, E_, G_, rho_,
                        shear_effects=True,
                        rotary_inertia=True,
                        gyroscopic=True)
    tim1 = ShaftElement(1, le_, i_d_, o_d_, E_, G_, rho_,
                        shear_effects=True,
                        rotary_inertia=True,
                        gyroscopic=True)

    shaft_elm = [tim0, tim1]
    return Rotor(shaft_elm, [], [])


def test_index_eigenvalues_rotor1(rotor1):
    evalues = np.array([-3.8 + 68.6j, -3.8 - 68.6j, -1.8 + 30.j, -1.8 - 30.j, -0.7 + 14.4j, -0.7 - 14.4j])
    evalues2 = np.array([0. + 68.7j, 0. - 68.7j, 0. + 30.1j, 0. - 30.1j, -0. + 14.4j, -0. - 14.4j])
    assert_almost_equal([4, 2, 0, 1, 3, 5], rotor1._index(evalues))
    assert_almost_equal([4, 2, 0, 1, 3, 5], rotor1._index(evalues2))


def test_mass_matrix_rotor1(rotor1):
    Mr1 = np.array([[ 1.421,  0.   ,  0.   ,  0.049,  0.496,  0.   ,  0.   , -0.031,  0.   ,  0.   ,  0.   ,  0.   ],
                    [ 0.   ,  1.421, -0.049,  0.   ,  0.   ,  0.496,  0.031,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
                    [ 0.   , -0.049,  0.002,  0.   ,  0.   , -0.031, -0.002,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
                    [ 0.049,  0.   ,  0.   ,  0.002,  0.031,  0.   ,  0.   , -0.002,  0.   ,  0.   ,  0.   ,  0.   ],
                    [ 0.496,  0.   ,  0.   ,  0.031,  2.841,  0.   ,  0.   ,  0.   ,  0.496,  0.   ,  0.   , -0.031],
                    [ 0.   ,  0.496, -0.031,  0.   ,  0.   ,  2.841,  0.   ,  0.   ,  0.   ,  0.496,  0.031,  0.   ],
                    [ 0.   ,  0.031, -0.002,  0.   ,  0.   ,  0.   ,  0.005,  0.   ,  0.   , -0.031, -0.002,  0.   ],
                    [-0.031,  0.   ,  0.   , -0.002,  0.   ,  0.   ,  0.   ,  0.005,  0.031,  0.   ,  0.   , -0.002],
                    [ 0.   ,  0.   ,  0.   ,  0.   ,  0.496,  0.   ,  0.   ,  0.031,  1.421,  0.   ,  0.   , -0.049],
                    [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.496, -0.031,  0.   ,  0.   ,  1.421,  0.049,  0.   ],
                    [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.031, -0.002,  0.   ,  0.   ,  0.049,  0.002,  0.   ],
                    [ 0.   ,  0.   ,  0.   ,  0.   , -0.031,  0.   ,  0.   , -0.002, -0.049,  0.   ,  0.   ,  0.002]])

    assert_almost_equal(rotor1.M(), Mr1, decimal=3)


@pytest.fixture
def rotor2():
    #  Rotor without damping with 2 shaft elements 1 disk and 2 bearings
    le_ = 0.25
    i_d_ = 0
    o_d_ = 0.05
    E_ = 211e9
    G_ = 81.2e9
    rho_ = 7810

    tim0 = ShaftElement(0, le_, i_d_, o_d_, E_, G_, rho_,
                        shear_effects=True,
                        rotary_inertia=True,
                        gyroscopic=True)
    tim1 = ShaftElement(1, le_, i_d_, o_d_, E_, G_, rho_,
                        shear_effects=True,
                        rotary_inertia=True,
                        gyroscopic=True)

    shaft_elm = [tim0, tim1]
    disk0 = DiskElement(1, rho_, 0.07, 0.05, 0.28)
    stf = 1e6
    bearing0 = BearingElement(0, kxx=stf, cxx=0)
    bearing1 = BearingElement(2, kxx=stf, cxx=0)

    return Rotor(shaft_elm, [disk0], [bearing0, bearing1])


def test_mass_matrix_rotor2(rotor2):
    Mr2 = np.array([[  1.421,   0.   ,   0.   ,   0.049,   0.496,   0.   ,   0.   ,  -0.031,   0.   ,   0.   ,   0.   ,   0.   ],
                    [  0.   ,   1.421,  -0.049,   0.   ,   0.   ,   0.496,   0.031,   0.   ,   0.   ,   0.   ,   0.   ,   0.   ],
                    [  0.   ,  -0.049,   0.002,   0.   ,   0.   ,  -0.031,  -0.002,   0.   ,   0.   ,   0.   ,   0.   ,   0.   ],
                    [  0.049,   0.   ,   0.   ,   0.002,   0.031,   0.   ,   0.   ,  -0.002,   0.   ,   0.   ,   0.   ,   0.   ],
                    [  0.496,   0.   ,   0.   ,   0.031,  35.431,   0.   ,   0.   ,   0.   ,   0.496,   0.   ,   0.   ,  -0.031],
                    [  0.   ,   0.496,  -0.031,   0.   ,   0.   ,  35.431,   0.   ,   0.   ,   0.   ,   0.496,   0.031,   0.   ],
                    [  0.   ,   0.031,  -0.002,   0.   ,   0.   ,   0.   ,   0.183,   0.   ,   0.   ,  -0.031,  -0.002,   0.   ],
                    [ -0.031,   0.   ,   0.   ,  -0.002,   0.   ,   0.   ,   0.   ,   0.183,   0.031,   0.   ,   0.   ,  -0.002],
                    [  0.   ,   0.   ,   0.   ,   0.   ,   0.496,   0.   ,   0.   ,   0.031,   1.421,   0.   ,   0.   ,  -0.049],
                    [  0.   ,   0.   ,   0.   ,   0.   ,   0.   ,   0.496,  -0.031,   0.   ,   0.   ,   1.421,   0.049,   0.   ],
                    [  0.   ,   0.   ,   0.   ,   0.   ,   0.   ,   0.031,  -0.002,   0.   ,   0.   ,   0.049,   0.002,   0.   ],
                    [  0.   ,   0.   ,   0.   ,   0.   ,  -0.031,   0.   ,   0.   ,  -0.002,  -0.049,   0.   ,   0.   ,   0.002]])
    assert_almost_equal(rotor2.M(), Mr2, decimal=3)


def test_a0_0_matrix_rotor2(rotor2):
    A0_0 = np.array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
    assert_almost_equal(rotor2.A()[:12, :12], A0_0, decimal=3)


def test_a0_1_matrix_rotor2(rotor2):
    A0_1 = np.array([[ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.]])
    assert_almost_equal(rotor2.A()[:12, 12:24], A0_1, decimal=3)


def test_a1_0_matrix_rotor2(rotor2):
    A1_0 = np.array([[  20.63 ,   -0.   ,    0.   ,    4.114,  -20.958,    0.   ,    0.   ,    1.11 ,    0.056,   -0.   ,   -0.   ,   -0.014],
                     [   0.   ,   20.63 ,   -4.114,    0.   ,   -0.   ,  -20.958,   -1.11 ,    0.   ,   -0.   ,    0.056,    0.014,    0.   ],
                     [   0.   ,  697.351, -131.328,    0.   ,   -0.   , -705.253,  -44.535,    0.   ,   -0.   ,    2.079,    0.596,    0.   ],
                     [-697.351,    0.   ,   -0.   , -131.328,  705.253,   -0.   ,   -0.   ,  -44.535,   -2.079,    0.   ,    0.   ,    0.596],
                     [   0.442,    0.   ,   -0.   ,    0.072,   -0.887,   -0.   ,   -0.   ,   -0.   ,    0.442,    0.   ,    0.   ,   -0.072],
                     [   0.   ,    0.442,   -0.072,    0.   ,   -0.   ,   -0.887,    0.   ,    0.   ,    0.   ,    0.442,    0.072,   -0.   ],
                     [   0.   ,    6.457,   -0.837,    0.   ,   -0.   ,    0.   ,   -1.561,    0.   ,   -0.   ,   -6.457,   -0.837,   -0.   ],
                     [  -6.457,   -0.   ,    0.   ,   -0.837,    0.   ,    0.   ,    0.   ,   -1.561,    6.457,    0.   ,    0.   ,   -0.837],
                     [   0.056,   -0.   ,    0.   ,    0.014,  -20.958,    0.   ,    0.   ,   -1.11 ,   20.63 ,    0.   ,    0.   ,   -4.114],
                     [   0.   ,    0.056,   -0.014,    0.   ,   -0.   ,  -20.958,    1.11 ,    0.   ,    0.   ,   20.63 ,    4.114,   -0.   ],
                     [  -0.   ,   -2.079,    0.596,   -0.   ,    0.   ,  705.253,  -44.535,   -0.   ,   -0.   , -697.351, -131.328,    0.   ],
                     [   2.079,    0.   ,   -0.   ,    0.596, -705.253,   -0.   ,    0.   ,  -44.535,  697.351,    0.   ,    0.   , -131.328]])
    assert_almost_equal(rotor2.A()[12:24, :12]/1e7, A1_0, decimal=3)


def test_a1_1_matrix_rotor2(rotor2):
    A1_1 = np.array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
    assert_almost_equal(rotor2.A()[12:24, 12:24] / 1e7, A1_1, decimal=3)


def test_evals_sorted_rotor2(rotor2):
    evals_sorted = np.array([  1.4667459679e-12 +215.3707255735j,   3.9623200168e-12 +215.3707255733j,
                               7.4569772223e-11 +598.0247411492j,   1.1024641658e-11 +598.0247411456j,
                               4.3188161105e-09+3956.2249777612j,   2.5852376472e-11+3956.2249797838j,
                               4.3188161105e-09-3956.2249777612j,   2.5852376472e-11-3956.2249797838j,
                               7.4569772223e-11 -598.0247411492j,   1.1024641658e-11 -598.0247411456j,
                               1.4667459679e-12 -215.3707255735j,   3.9623200168e-12 -215.3707255733j])

    evals_sorted_w_10000 = np.array([ -4.838034e-14  +34.822138j,  -5.045245e-01 +215.369011j,
                                      5.045245e-01 +215.369011j,   8.482603e-08+3470.897616j,
                                      4.878990e-07+3850.212629j,   4.176291e+01+3990.22903j ,
                                      4.176291e+01-3990.22903j ,   4.878990e-07-3850.212629j,
                                      8.482603e-08-3470.897616j,   5.045245e-01 -215.369011j,
                                      -5.045245e-01 -215.369011j,  -4.838034e-14  -34.822138j])

    rotor2_evals, rotor2_evects = rotor2._eigen()
    assert_allclose(rotor2_evals, evals_sorted, rtol=1e-3)
    assert_allclose(rotor2.evalues, evals_sorted, rtol=1e-3)
    rotor2.w = 10000
    assert_allclose(rotor2.evalues, evals_sorted_w_10000, rtol=1e-1)


@pytest.fixture
def rotor3():
    #  Rotor without damping with 6 shaft elements 2 disks and 2 bearings
    i_d = 0
    o_d = 0.05
    E = 211e9
    Gs = 81.2e9
    rho = 7810
    n = 6
    nelem = [x for x in range(n)]
    L = [0.25 for i in range(n)]

    shaft_elem = [ShaftElement(n, l, i_d, o_d, E, Gs, rho,
                               shear_effects=True,
                               rotary_inertia=True,
                               gyroscopic=True) for n, l in zip(nelem, L)]

    disk0 = DiskElement(2, rho, 0.07, 0.05, 0.28)
    disk1 = DiskElement(4, rho, 0.07, 0.05, 0.35)

    stfx = 1e6
    stfy = 0.8e6
    bearing0 = BearingElement(0, kxx=stfx, kyy=stfy, cxx=0)
    bearing1 = BearingElement(6, kxx=stfx, kyy=stfy, cxx=0)

    return Rotor(shaft_elem, [disk0, disk1], [bearing0, bearing1])


def test_evects_sorted_rotor3(rotor3):
    evects_sorted = np.array([[ -4.056e-16 +8.044e-15j,   6.705e-19 -1.153e-03j,  -2.140e-15 +2.486e-14j,  -7.017e-17 +8.665e-04j],
                              [ -4.507e-17 -1.454e-03j,   5.888e-16 -1.658e-14j,  -1.698e-16 +9.784e-04j,   6.498e-16 +6.575e-14j],
                              [  3.930e-16 +4.707e-03j,  -1.916e-15 +5.753e-14j,   1.493e-17 +3.452e-04j,   2.575e-16 +1.289e-14j],
                              [ -1.988e-15 +3.816e-14j,  -5.225e-17 -4.648e-03j,  -1.167e-16 -3.922e-14j,   1.538e-16 -1.023e-04j],
                              [ -8.603e-16 +1.698e-14j,  -3.537e-17 -2.271e-03j,  -2.048e-15 +1.606e-14j,   1.939e-17 +8.099e-04j],
                              [ -1.022e-16 -2.586e-03j,   1.047e-15 -3.047e-14j,  -1.993e-16 +8.642e-04j,   5.357e-16 +6.104e-14j],
                              [  3.437e-16 +4.153e-03j,  -1.638e-15 +5.135e-14j,  -1.607e-17 +6.848e-04j,   4.770e-16 +3.704e-14j],
                              [ -1.736e-15 +3.413e-14j,  -1.168e-16 -4.098e-03j,   8.543e-16 -4.710e-14j,   1.840e-16 -4.807e-04j],
                              [ -1.298e-15 +2.574e-14j,  -7.387e-17 -3.118e-03j,  -1.588e-15 -7.947e-15j,   5.808e-17 +5.782e-04j],
                              [ -1.974e-16 -3.445e-03j,   1.381e-15 -4.169e-14j,  -1.433e-16 +5.933e-04j,   3.236e-16 +4.312e-14j],
                              [  2.387e-16 +2.529e-03j,  -1.028e-15 +3.221e-14j,  -2.678e-16 +1.561e-03j,   1.039e-15 +1.022e-13j],
                              [ -1.085e-15 +2.105e-14j,  -3.912e-17 -2.485e-03j,   3.717e-15 -4.134e-14j,   5.483e-17 -1.463e-03j],
                              [ -1.457e-15 +2.827e-14j,  -7.171e-17 -3.463e-03j,  -3.515e-16 -1.138e-14j,   3.815e-17 +1.101e-04j],
                              [ -2.795e-16 -3.800e-03j,   1.573e-15 -4.573e-14j,  -5.757e-17 +1.120e-04j,   3.794e-17 +1.081e-14j],
                              [  6.589e-18 +2.699e-04j,  -1.258e-16 +5.309e-15j,  -5.315e-16 +2.124e-03j,   1.364e-15 +1.555e-13j],
                              [ -2.067e-16 +3.324e-15j,  -3.704e-19 -2.394e-04j,   5.665e-15 -1.530e-14j,  -2.417e-16 -2.095e-03j],
                              [ -1.287e-15 +2.544e-14j,  -2.928e-17 -3.224e-03j,   1.039e-15 +1.573e-15j,  -3.299e-17 -3.849e-04j],
                              [ -1.851e-16 -3.567e-03j,   1.468e-15 -4.382e-14j,   1.043e-16 -3.941e-04j,  -2.973e-16 -2.819e-14j],
                              [ -1.492e-16 -2.150e-03j,   8.603e-16 -2.432e-14j,  -4.512e-16 +1.755e-03j,   1.236e-15 +1.412e-13j],
                              [  8.553e-16 -1.661e-14j,   1.701e-17 +2.167e-03j,   4.628e-15 +4.535e-14j,  -2.653e-16 -1.672e-03j],
                              [ -1.023e-15 +2.015e-14j,   3.903e-18 -2.426e-03j,   1.846e-15 +8.393e-15j,   6.506e-18 -6.765e-04j],
                              [ -9.796e-17 -2.771e-03j,   1.179e-15 -3.432e-14j,   1.394e-16 -7.208e-04j,  -5.197e-16 -5.518e-14j],
                              [ -2.651e-16 -4.008e-03j,   1.614e-15 -4.657e-14j,  -1.703e-16 +9.358e-04j,   5.812e-16 +8.236e-14j],
                              [  1.629e-15 -3.212e-14j,   1.655e-16 +4.011e-03j,   2.089e-15 +5.726e-14j,  -1.483e-16 -7.478e-04j],
                              [ -5.683e-16 +1.120e-14j,   1.973e-18 -1.316e-03j,   2.135e-15 +2.161e-14j,  -1.782e-16 -8.042e-04j],
                              [ -1.326e-16 -1.661e-03j,   6.747e-16 -2.122e-14j,   2.023e-16 -9.021e-04j,  -6.436e-16 -7.128e-14j],
                              [ -2.641e-16 -4.641e-03j,   1.899e-15 -5.464e-14j,  -8.833e-17 +6.219e-04j,   3.673e-16 +5.731e-14j],
                              [  1.912e-15 -3.674e-14j,   8.212e-17 +4.639e-03j,   1.118e-15 +5.106e-14j,  -1.381e-16 -3.957e-04j],
                              [ -6.649e-13 -3.259e-14j,   9.993e-02 +1.484e-16j,  -6.328e-12 -5.265e-13j,  -2.377e-01 -2.190e-14j],
                              [  1.202e-01 +3.939e-15j,   1.437e-12 +4.632e-14j,  -2.490e-01 +1.433e-14j,  -1.804e-11 +1.579e-13j],
                              [ -3.890e-01 -1.104e-16j,  -4.986e-12 -1.506e-13j,  -8.786e-02 +2.066e-14j,  -3.536e-12 +4.313e-14j],
                              [ -3.154e-12 -1.584e-13j,   4.028e-01 -4.557e-16j,   9.983e-12 -3.182e-14j,   2.806e-02 +5.927e-14j],
                              [ -1.403e-12 -7.024e-14j,   1.968e-01 -9.752e-16j,  -4.087e-12 -5.170e-13j,  -2.222e-01 -8.547e-15j],
                              [  2.138e-01 -3.508e-16j,   2.641e-12 +8.131e-14j,  -2.199e-01 +3.955e-15j,  -1.674e-11 +1.529e-13j],
                              [ -3.432e-01 +1.993e-15j,  -4.450e-12 -1.318e-13j,  -1.743e-01 +2.838e-14j,  -1.016e-11 +9.643e-14j],
                              [ -2.821e-12 -1.418e-13j,   3.552e-01 +1.011e-15j,   1.199e-11 +2.189e-13j,   1.319e-01 +5.933e-14j],
                              [ -2.127e-12 -1.070e-13j,   2.702e-01 -1.220e-15j,   2.023e-12 -4.081e-13j,  -1.586e-01 +2.107e-14j],
                              [  2.847e-01 +5.856e-16j,   3.613e-12 +1.088e-13j,  -1.510e-01 -5.642e-15j,  -1.183e-11 +1.084e-13j],
                              [ -2.090e-01 -6.114e-16j,  -2.791e-12 -8.398e-14j,  -3.973e-01 -4.666e-15j,  -2.804e-11 +2.739e-13j],
                              [ -1.740e-12 -9.060e-14j,   2.154e-01 +2.735e-15j,   1.052e-11 +9.056e-13j,   4.013e-01 +2.727e-14j],
                              [ -2.336e-12 -1.183e-13j,   3.001e-01 -1.686e-15j,   2.896e-12 -9.755e-14j,  -3.019e-02 +1.411e-14j],
                              [  3.141e-01 +3.027e-16j,   3.963e-12 +1.216e-13j,  -2.852e-02 -9.895e-15j,  -2.965e-12 +2.787e-14j],
                              [ -2.231e-02 -7.712e-16j,  -4.601e-13 -1.276e-14j,  -5.407e-01 -1.298e-14j,  -4.266e-11 +3.859e-13j],
                              [ -2.747e-13 -1.805e-14j,   2.074e-02 +1.739e-15j,   3.895e-12 +1.389e-12j,   5.747e-01 -1.335e-14j],
                              [ -2.103e-12 -1.056e-13j,   2.794e-01 +4.152e-15j,  -4.003e-13 +2.638e-13j,   1.056e-01 -1.101e-14j],
                              [  2.948e-01 +2.284e-15j,   3.797e-12 +1.154e-13j,   1.003e-01 +2.587e-15j,   7.733e-12 -7.168e-14j],
                              [  1.777e-01 -1.271e-15j,   2.108e-12 +6.492e-14j,  -4.467e-01 -1.871e-14j,  -3.874e-11 +3.205e-13j],
                              [  1.373e-12 +6.849e-14j,  -1.877e-01 +3.120e-15j,  -1.154e-11 +1.153e-12j,   4.588e-01 -3.120e-14j],
                              [ -1.665e-12 -8.544e-14j,   2.102e-01 +9.552e-16j,  -2.136e-12 +4.515e-13j,   1.856e-01 -4.985e-15j],
                              [  2.290e-01 -6.196e-16j,   2.974e-12 +8.935e-14j,   1.835e-01 -7.359e-15j,   1.514e-11 -1.221e-13j],
                              [  3.313e-01 +2.523e-16j,   4.036e-12 +1.236e-13j,  -2.382e-01 +6.579e-15j,  -2.259e-11 +1.654e-13j],
                              [  2.655e-12 +1.347e-13j,  -3.476e-01 +8.013e-16j,  -1.457e-11 +5.232e-13j,   2.051e-01 -1.595e-14j],
                              [ -9.256e-13 -4.619e-14j,   1.141e-01 +1.417e-15j,  -5.501e-12 +5.233e-13j,   2.206e-01 -2.267e-15j],
                              [  1.373e-01 -4.564e-15j,   1.838e-12 +5.302e-14j,   2.296e-01 -8.382e-15j,   1.955e-11 -1.490e-13j],
                              [  3.836e-01 +1.840e-16j,   4.735e-12 +1.445e-13j,  -1.583e-01 +9.794e-15j,  -1.572e-11 +1.066e-13j],
                              [  3.037e-12 +1.550e-13j,  -4.020e-01 +1.116e-15j,  -1.300e-11 +2.719e-13j,   1.086e-01 -6.340e-15j]])

    rotor3_evals, rotor3_evects = rotor3._eigen()
    mac1 = MAC_modes(evects_sorted, rotor3_evects[:, :4], plot=False)
    mac2 = MAC_modes(evects_sorted, rotor3.evectors[:, :4], plot=False)
    assert_allclose(mac1.diagonal(), np.ones_like(mac1.diagonal()))
    assert_allclose(mac2.diagonal(), np.ones_like(mac1.diagonal()))


def test_evects_not_sorted_rotor3(rotor3):
    evects = np.array([[  8.687e-15 +1.258e-16j,   8.687e-15 -1.258e-16j,  -2.333e-18 +1.153e-03j,  -2.333e-18 -1.153e-03j],
                       [  1.454e-03 +5.812e-17j,   1.454e-03 -5.812e-17j,  -1.463e-16 -8.815e-15j,  -1.463e-16 +8.815e-15j],
                       [ -4.707e-03 -2.106e-16j,  -4.707e-03 +2.106e-16j,   4.482e-16 +2.901e-14j,   4.482e-16 -2.901e-14j],
                       [  3.574e-14 +4.953e-16j,   3.574e-14 -4.953e-16j,  -2.464e-17 +4.648e-03j,  -2.464e-17 -4.648e-03j],
                       [  1.720e-14 +2.694e-16j,   1.720e-14 -2.694e-16j,   4.044e-17 +2.271e-03j,   4.044e-17 -2.271e-03j],
                       [  2.586e-03 +1.050e-16j,   2.586e-03 -1.050e-16j,  -2.640e-16 -1.594e-14j,  -2.640e-16 +1.594e-14j],
                       [ -4.153e-03 -2.142e-16j,  -4.153e-03 +2.142e-16j,   3.761e-16 +2.581e-14j,   3.761e-16 -2.581e-14j],
                       [  3.152e-14 +4.626e-16j,   3.152e-14 -4.626e-16j,   1.785e-17 +4.098e-03j,   1.785e-17 -4.098e-03j],
                       [  2.392e-14 +3.661e-16j,   2.392e-14 -3.661e-16j,   9.092e-17 +3.118e-03j,   9.092e-17 -3.118e-03j],
                       [  3.445e-03 +1.574e-16j,   3.445e-03 -1.574e-16j,  -3.234e-16 -2.130e-14j,  -3.234e-16 +2.130e-14j],
                       [ -2.529e-03 -1.202e-16j,  -2.529e-03 +1.202e-16j,   2.406e-16 +1.578e-14j,   2.406e-16 -1.578e-14j],
                       [  1.908e-14 +2.843e-16j,   1.908e-14 -2.843e-16j,   7.861e-18 +2.485e-03j,   7.861e-18 -2.485e-03j],
                       [  2.674e-14 +3.956e-16j,   2.674e-14 -3.956e-16j,   2.159e-17 +3.463e-03j,   2.159e-17 -3.463e-03j],
                       [  3.800e-03 +1.949e-16j,   3.800e-03 -1.949e-16j,  -3.451e-16 -2.344e-14j,  -3.451e-16 +2.344e-14j],
                       [ -2.699e-04 -1.405e-17j,  -2.699e-04 +1.405e-17j,   2.133e-17 +1.843e-15j,   2.133e-17 -1.843e-15j],
                       [  2.282e-15 +2.879e-17j,   2.282e-15 -2.879e-17j,   1.315e-17 +2.394e-04j,   1.315e-17 -2.394e-04j],
                       [  2.474e-14 +3.833e-16j,   2.474e-14 -3.833e-16j,   3.889e-17 +3.224e-03j,   3.889e-17 -3.224e-03j],
                       [  3.567e-03 +1.651e-16j,   3.567e-03 -1.651e-16j,  -3.314e-16 -2.209e-14j,  -3.314e-16 +2.209e-14j],
                       [  2.150e-03 +1.014e-16j,   2.150e-03 -1.014e-16j,  -2.078e-16 -1.325e-14j,  -2.078e-16 +1.325e-14j],
                       [ -1.611e-14 -2.197e-16j,  -1.611e-14 +2.197e-16j,   3.318e-17 -2.167e-03j,   3.318e-17 +2.167e-03j],
                       [  1.855e-14 +2.784e-16j,   1.855e-14 -2.784e-16j,   3.168e-17 +2.426e-03j,   3.168e-17 -2.426e-03j],
                       [  2.771e-03 +1.080e-16j,   2.771e-03 -1.080e-16j,  -3.022e-16 -1.710e-14j,  -3.022e-16 +1.710e-14j],
                       [  4.008e-03 +1.663e-16j,   4.008e-03 -1.663e-16j,  -4.061e-16 -2.450e-14j,  -4.061e-16 +2.450e-14j],
                       [ -3.032e-14 -4.682e-16j,  -3.032e-14 +4.682e-16j,  -4.405e-17 -4.011e-03j,  -4.405e-17 +4.011e-03j],
                       [  1.023e-14 +1.299e-16j,   1.023e-14 -1.299e-16j,  -1.404e-17 +1.316e-03j,  -1.404e-17 -1.316e-03j],
                       [  1.661e-03 +7.706e-17j,   1.661e-03 -7.706e-17j,  -1.644e-16 -1.016e-14j,  -1.644e-16 +1.016e-14j],
                       [  4.641e-03 +1.936e-16j,   4.641e-03 -1.936e-16j,  -4.568e-16 -2.886e-14j,  -4.568e-16 +2.886e-14j],
                       [ -3.560e-14 -5.128e-16j,  -3.560e-14 +5.128e-16j,  -5.128e-18 -4.639e-03j,  -5.128e-18 +4.639e-03j],
                       [  7.029e-15 -7.180e-13j,   7.029e-15 +7.180e-13j,   9.993e-02 +2.666e-16j,   9.993e-02 -2.666e-16j],
                       [ -9.755e-16 -1.202e-01j,  -9.755e-16 +1.202e-01j,  -7.638e-13 +6.960e-15j,  -7.638e-13 -6.960e-15j],
                       [  9.233e-17 +3.890e-01j,   9.233e-17 -3.890e-01j,   2.514e-12 -2.133e-14j,   2.514e-12 +2.133e-14j],
                       [  2.854e-14 -2.954e-12j,   2.854e-14 +2.954e-12j,   4.028e-01 +4.732e-16j,   4.028e-01 -4.732e-16j],
                       [  1.333e-14 -1.421e-12j,   1.333e-14 +1.421e-12j,   1.968e-01 +7.918e-16j,   1.968e-01 -7.918e-16j],
                       [ -2.040e-16 -2.138e-01j,  -2.040e-16 +2.138e-01j,  -1.381e-12 +1.111e-14j,  -1.381e-12 -1.111e-14j],
                       [ -3.914e-16 +3.432e-01j,  -3.914e-16 -3.432e-01j,   2.236e-12 -1.881e-14j,   2.236e-12 +1.881e-14j],
                       [  2.624e-14 -2.605e-12j,   2.624e-14 +2.605e-12j,   3.552e-01 -9.875e-16j,   3.552e-01 +9.875e-16j],
                       [  1.979e-14 -1.977e-12j,   1.979e-14 +1.977e-12j,   2.702e-01 +2.212e-16j,   2.702e-01 -2.212e-16j],
                       [  8.340e-16 -2.847e-01j,   8.340e-16 +2.847e-01j,  -1.846e-12 +1.510e-14j,  -1.846e-12 -1.510e-14j],
                       [ -7.266e-16 +2.090e-01j,  -7.266e-16 -2.090e-01j,   1.367e-12 -1.096e-14j,   1.367e-12 +1.096e-14j],
                       [  1.599e-14 -1.577e-12j,   1.599e-14 +1.577e-12j,   2.154e-01 -2.031e-15j,   2.154e-01 +2.031e-15j],
                       [  2.272e-14 -2.210e-12j,   2.272e-14 +2.210e-12j,   3.001e-01 -5.059e-16j,   3.001e-01 +5.059e-16j],
                       [ -4.550e-17 -3.141e-01j,  -4.550e-17 +3.141e-01j,  -2.031e-12 +1.788e-14j,  -2.031e-12 -1.788e-14j],
                       [ -3.528e-16 +2.231e-02j,  -3.528e-16 -2.231e-02j,   1.597e-13 -1.187e-15j,   1.597e-13 +1.187e-15j],
                       [  2.802e-15 -1.886e-13j,   2.802e-15 +1.886e-13j,   2.074e-02 -1.805e-15j,   2.074e-02 +1.805e-15j],
                       [  2.063e-14 -2.045e-12j,   2.063e-14 +2.045e-12j,   2.794e-01 -1.021e-15j,   2.794e-01 +1.021e-15j],
                       [  1.529e-15 -2.948e-01j,   1.529e-15 +2.948e-01j,  -1.914e-12 +1.487e-14j,  -1.914e-12 -1.487e-14j],
                       [ -9.366e-17 -1.777e-01j,  -9.366e-17 +1.777e-01j,  -1.148e-12 +9.371e-15j,  -1.148e-12 -9.371e-15j],
                       [ -1.216e-14 +1.332e-12j,  -1.216e-14 -1.332e-12j,  -1.877e-01 -2.057e-15j,  -1.877e-01 +2.057e-15j],
                       [  1.568e-14 -1.534e-12j,   1.568e-14 +1.534e-12j,   2.102e-01 -5.493e-16j,   2.102e-01 +5.493e-16j],
                       [ -3.577e-16 -2.290e-01j,  -3.577e-16 +2.290e-01j,  -1.481e-12 +1.258e-14j,  -1.481e-12 -1.258e-14j],
                       [ -1.435e-15 -3.313e-01j,  -1.435e-15 +3.313e-01j,  -2.123e-12 +1.811e-14j,  -2.123e-12 -1.811e-14j],
                       [ -2.425e-14 +2.506e-12j,  -2.425e-14 -2.506e-12j,  -3.476e-01 -2.110e-15j,  -3.476e-01 +2.110e-15j],
                       [  8.521e-15 -8.455e-13j,   8.521e-15 +8.455e-13j,   1.141e-01 -5.069e-16j,   1.141e-01 +5.069e-16j],
                       [ -5.894e-16 -1.373e-01j,  -5.894e-16 +1.373e-01j,  -8.805e-13 +8.027e-15j,  -8.805e-13 -8.027e-15j],
                       [ -2.978e-16 -3.836e-01j,  -2.978e-16 +3.836e-01j,  -2.501e-12 +2.165e-14j,  -2.501e-12 -2.165e-14j],
                       [ -2.913e-14 +2.942e-12j,  -2.913e-14 -2.942e-12j,  -4.020e-01 +2.776e-16j,  -4.020e-01 -2.776e-16j]])

    rotor3_evals, rotor3_evects = rotor3._eigen(sorted_=False)
    mac1 = MAC_modes(evects, rotor3_evects[:, :4], plot=False)
    assert_allclose(mac1.diagonal(), np.ones_like(mac1.diagonal()))


def test_kappa_rotor3(rotor3):
    assert_allclose(rotor3.kappa(0, 0)['Frequency'], 82.653037, rtol=1e-3)
    assert_allclose(rotor3.kappa(0, 0)['Major axes'], 0.001454062985920231, rtol=1e-3)
    assert_allclose(rotor3.kappa(0, 0)['Minor axes'], 2.0579515874459978e-11, rtol=1e-3, atol=1e-6)
    assert_allclose(rotor3.kappa(0, 0)['kappa'], -1.415311171090584e-08, rtol=1e-3, atol=1e-6)

    rotor3.w = 2000
    assert_allclose(rotor3.kappa(0, 0)['Frequency'], 78.149731, rtol=1e-3)
    assert_allclose(rotor3.kappa(0, 0)['Major axes'], 0.0012684572844586523, rtol=1e-3)
    assert_allclose(rotor3.kappa(0, 0)['Minor axes'], 0.0006038839712968117, rtol=1e-3)
    assert_allclose(rotor3.kappa(0, 0)['kappa'], -0.4760774987819437, rtol=1e-3)

    assert_allclose(rotor3.kappa(0, 1)['Frequency'], 88.08130950672094, rtol=1e-3)
    assert_allclose(rotor3.kappa(0, 1)['Major axes'], 0.0009748776471415336, rtol=1e-3)
    assert_allclose(rotor3.kappa(0, 1)['Minor axes'], 0.0009175930931051902, rtol=1e-3)
    assert_allclose(rotor3.kappa(0, 1)['kappa'], 0.9412392373501342, rtol=1e-3)

    assert_allclose(rotor3.kappa(1, 1)['Frequency'], 88.08130950672094, rtol=1e-3)
    assert_allclose(rotor3.kappa(1, 1)['Major axes'], 0.0018353712883928638, rtol=1e-3)
    assert_allclose(rotor3.kappa(1, 1)['Minor axes'], 0.0015705146844725273, rtol=1e-3)
    assert_allclose(rotor3.kappa(1, 1)['kappa'], 0.8556931746751595, rtol=1e-3)


def test_kappa_mode_rotor3(rotor3):
    rotor3.w = 2000
    assert_allclose(rotor3.kappa_mode(0), [-0.4760774987819437,
                                           -0.5530692751423727,
                                           -0.5810044451669006,
                                           -0.5850566835145273,
                                           -0.5570616152127553,
                                           -0.49445836271656823,
                                           -0.3367646671198142], rtol=1e-3)

    assert_allclose(rotor3.kappa_mode(1), [0.9412392373501342,
                                           0.8556931746751595,
                                           0.8312076693440857,
                                           0.8335994875395676,
                                           0.8684698141762651,
                                           0.9403875416867278,
                                           0.8964329651295495], rtol=1e-3)


#  TODO implement more tests using a simple rotor with 2 elements and one disk
#  TODO add test for damped case

