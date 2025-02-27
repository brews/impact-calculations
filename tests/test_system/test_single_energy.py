"""System smoke tests for a single, diagnostic run for the energy sector.

These will likely fail if run as installed package as we unfortunately make
strong assumptions about directory structure. These are also smoke tests,
and are not comprehensive.
"""

from pathlib import Path

import pytest
import xarray as xr
import numpy as np
import numpy.testing as npt

from utils import tmpdir_projection


pytestmark = pytest.mark.imperics_shareddir


@pytest.fixture(scope="module")
def projection_netcdf():
    """Runs the projection in tmpdir, gets results netCDF, cleans output on exit
    """
    run_configs = {
        "mode": "writecalcs",
        "singledir": "single",
        "filter-region": "USA.14.608",
        "do_farmers": False,
        "do_historical": False,
        "deltamethod": False,
        "econcovar": {"class": "mean", "length": 15},
        "climcovar": {"class": "mean", "length": 15},
        "loggdppc-delta": 9.087,
        "timerate": "year",
        "climate": [
            "tas",
            "tas-poly-2",
            "tas-cdd-20",
            "tas-cdd-20-poly-2",
            "tas-hdd-20",
            "tas-hdd-20-poly-2",
        ],
        "models": [
            {
                "csvvs": "social/parameters/energy/projectionT/*.csvv",
                "covariates": [
                    {
                        "incbin": [
                            "-inf",
                            7.246,
                            7.713,
                            8.136,
                            8.475,
                            8.776,
                            9.087,
                            9.385,
                            9.783,
                            10.198,
                            "inf",
                        ]
                    },
                    {
                        "year*incbin": [
                            "-inf",
                            7.246,
                            7.713,
                            8.136,
                            8.475,
                            8.776,
                            9.087,
                            9.385,
                            9.783,
                            10.198,
                            "inf",
                        ]
                    },
                    "climtas-cdd-20",
                    "climtas-hdd-20",
                    {
                        "climtas-cdd-20*incbin": [
                            "-inf",
                            7.246,
                            7.713,
                            8.136,
                            8.475,
                            8.776,
                            9.087,
                            9.385,
                            9.783,
                            10.198,
                            "inf",
                        ]
                    },
                    {
                        "climtas-hdd-20*incbin": [
                            "-inf",
                            7.246,
                            7.713,
                            8.136,
                            8.475,
                            8.776,
                            9.087,
                            9.385,
                            9.783,
                            10.198,
                            "inf",
                        ]
                    },
                    {
                        "loggdppc-shifted*incbin": [
                            "-inf",
                            7.246,
                            7.713,
                            8.136,
                            8.475,
                            8.776,
                            9.087,
                            9.385,
                            9.783,
                            10.198,
                            "inf",
                        ]
                    },
                    {
                        "loggdppc-shifted*year*incbin": [
                            "-inf",
                            7.246,
                            7.713,
                            8.136,
                            8.475,
                            8.776,
                            9.087,
                            9.385,
                            9.783,
                            10.198,
                            "inf",
                        ]
                    },
                ],
                "clipping": False,
                "description": "Change in energy usage driven by a single day's mean temperature",
                "depenunit": "kWh/pc",
                "specifications": {
                    "tas": {
                        "description": "Uninteracted term.",
                        "indepunit": "C",
                        "functionalform": "polynomial",
                        "variable": "tas",
                    },
                    "hdd-20": {
                        "description": "Below 20C days.",
                        "indepunit": "C",
                        "functionalform": "polynomial",
                        "variable": "tas-hdd-20",
                    },
                    "cdd-20": {
                        "description": "Above 20C days.",
                        "indepunit": "C",
                        "functionalform": "polynomial",
                        "variable": "tas-cdd-20",
                    },
                },
                "calculation": [
                    {
                        "Sum": [
                            {"YearlyApply": {"model": "tas"}},
                            {"YearlyApply": {"model": "hdd-20"}},
                            {"YearlyApply": {"model": "cdd-20"}},
                        ]
                    },
                    "Rebase",
                ],
            }
        ],
    }
    # Trigger projection run in temprary directory:
    with tmpdir_projection(run_configs, "single energy test") as tmpdirname:
        results_nc_path = Path(
            tmpdirname,
            "single/rcp85/CCSM4/high/SSP3",
            "FD_FGLS_inter_climGMFD_Exclude_all-issues_break2_semi-parametric_poly2_OTHERIND_other_energy_TINV_clim_income_spline_lininter.nc4",
        )
        yield xr.open_dataset(results_nc_path)


def test_region(projection_netcdf):
    """Test the 'regions' dimension of output netCDF
    """
    assert str(projection_netcdf["regions"].values.item()) == "USA.14.608"


class TestYear:
    """Test netCDF output 'year' dimension
    """

    target_variable = "year"

    def test_shape(self, projection_netcdf):
        """Test variable array shape"""
        assert projection_netcdf[self.target_variable].values.shape == (120,)

    def test_head(self, projection_netcdf):
        """Test head of variable array"""
        npt.assert_array_equal(
            projection_netcdf[self.target_variable].values[:3],
            np.array([1981, 1982, 1983]),
        )

    def test_tail(self, projection_netcdf):
        """Test tail of variable array"""
        npt.assert_array_equal(
            projection_netcdf[self.target_variable].values[-3:],
            np.array([2098, 2099, 2100]),
        )


class TestRebased:
    """Test netCDF output 'rebased' variable
    """

    target_variable = "rebased"
    atol = 1e-3
    rtol = 0

    def test_shape(self, projection_netcdf):
        """Test variable array shape"""
        assert projection_netcdf[self.target_variable].values.shape == (120, 1)

    def test_head(self, projection_netcdf):
        """Test head of variable array"""
        npt.assert_allclose(
            projection_netcdf[self.target_variable].values[:3],
            np.array([[20.576303, 108.616135, 451.51030]]).T,
            atol=self.atol,
            rtol=self.rtol,
        )

    def test_tail(self, projection_netcdf):
        """Test tail of variable array"""
        npt.assert_allclose(
            projection_netcdf[self.target_variable].values[-3:],
            np.array([[-2595.0160, -3619.1338, -2849.8433]]).T,
            atol=self.atol,
            rtol=self.rtol,
        )
