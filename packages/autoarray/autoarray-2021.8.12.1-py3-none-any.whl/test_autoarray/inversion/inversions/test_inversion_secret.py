import autoarray as aa
from autoarray.inversion.inversion import inversion_secret
import numpy as np
import pytest


class TestWTildeInterferometer:
    def test__gives_correct_matrix_for_simple_values(self):

        sigma_real = np.array([1.0, 2.0, 3.0])
        uv_wavelengths = np.array([[0.0001, 2.0, 3000.0], [3000.0, 2.0, 0.0001]])

        grid = aa.Grid2D.uniform(shape_native=(2, 2), pixel_scales=0.0005)

        w_tilde = inversion_secret.w_tilde_interferometer_from(
            sigma_real=sigma_real, uv_wavelengths=uv_wavelengths, grid_radians_slim=grid
        )

        assert w_tilde == pytest.approx(
            np.array(
                [
                    [1.25, 0.75, 1.24997, 0.74998],
                    [0.75, 1.25, 0.74998, 1.24997],
                    [1.24994, 0.74998, 1.25, 0.75],
                    [0.74998, 1.24997, 0.75, 1.25],
                ]
            ),
            1.0e-4,
        )

    def test__w_tilde_via_preload_same_as_w_tilde(self):

        sigma_real = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        uv_wavelengths = np.array(
            [
                [0.0001, 2.0, 3000.0, 50000.0, 200000.0],
                [3000.0, 2.0, 0.0001, 10.0, 5000.0],
            ]
        )

        grid = aa.Grid2D.uniform(shape_native=(3, 3), pixel_scales=0.0005)

        w_tilde = inversion_secret.w_tilde_interferometer_from(
            sigma_real=sigma_real, uv_wavelengths=uv_wavelengths, grid_radians_slim=grid
        )

        w_tilde_preload = inversion_secret.w_tilde_preload_interferometer_from(
            sigma_real=sigma_real,
            uv_wavelengths=uv_wavelengths,
            shape_masked_pixels_2d=(3, 3),
            grid_radians_2d=grid.native,
        )

        native_index_for_slim_index = np.array(
            [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        )

        w_tilde_via_preload = inversion_secret.w_tilde_interferometer_via_preload_from(
            w_tilde_preload=w_tilde_preload,
            native_index_for_slim_index=native_index_for_slim_index,
        )

        assert (w_tilde == w_tilde_via_preload).all()

    def test__curvature_matrix_via_w_tilde_preload_from(self):

        sigma_real = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        uv_wavelengths = np.array(
            [
                [0.0001, 2.0, 3000.0, 50000.0, 200000.0],
                [3000.0, 2.0, 0.0001, 10.0, 5000.0],
            ]
        )

        grid = aa.Grid2D.uniform(shape_native=(3, 3), pixel_scales=0.0005)

        w_tilde = inversion_secret.w_tilde_interferometer_from(
            sigma_real=sigma_real, uv_wavelengths=uv_wavelengths, grid_radians_slim=grid
        )

        mapping_matrix = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 0.0],
            ]
        )

        curvature_matrix_via_w_tilde = aa.util.inversion.curvature_matrix_via_w_tilde_from(
            w_tilde=w_tilde, mapping_matrix=mapping_matrix
        )

        w_tilde_preload = inversion_secret.w_tilde_preload_interferometer_from(
            sigma_real=sigma_real,
            uv_wavelengths=uv_wavelengths,
            shape_masked_pixels_2d=(3, 3),
            grid_radians_2d=grid.native,
        )

        pixelization_index_for_sub_slim_index = np.array([0, 2, 1, 1, 2, 2, 0, 2, 0])

        native_index_for_slim_index = np.array(
            [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        )

        curvature_matrix_via_preload = inversion_secret.curvature_matrix_via_w_tilde_preload_interferometer_from(
            w_tilde_preload=w_tilde_preload,
            pixelization_index_for_sub_slim_index=pixelization_index_for_sub_slim_index,
            native_index_for_slim_index=native_index_for_slim_index,
            pixelization_pixels=3,
        )

        assert curvature_matrix_via_w_tilde == pytest.approx(
            curvature_matrix_via_preload, 1.0e-4
        )
