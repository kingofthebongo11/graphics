import numpy as np

from functions_for_tab2.models import ComputedSegment
from functions_for_tab2.stitch import stitch_segments


def test_stitch_with_continuity_adjustment():
    seg1 = ComputedSegment(
        X=np.array([0.0, 1.0, 2.0]),
        Y=np.array([0.0, 1.0, 4.0]),
    )
    seg2 = ComputedSegment(
        X=np.array([2.0 + 1e-9, 3.0, 4.0]),
        Y=np.array([4.0, 9.0, 16.0]),
    )

    stitched = stitch_segments([seg1, seg2], ["X", "X"], True, tol=1e-8)

    assert np.allclose(stitched.X, [0.0, 1.0, 2.0, 3.0, 4.0])
    assert np.allclose(stitched.Y, [0.0, 1.0, 4.0, 9.0, 16.0])


def test_stitch_without_continuity():
    seg1 = ComputedSegment(
        X=np.array([0.0, 1.0, 2.0]),
        Y=np.array([0.0, 1.0, 4.0]),
    )
    seg2 = ComputedSegment(
        X=np.array([2.0 + 1e-9, 3.0, 4.0]),
        Y=np.array([4.0, 9.0, 16.0]),
    )

    stitched = stitch_segments([seg1, seg2], ["X", "X"], False, tol=1e-8)

    assert np.allclose(stitched.X, [0.0, 1.0, 2.0, 2.0 + 1e-9, 3.0, 4.0])
    assert np.allclose(stitched.Y, [0.0, 1.0, 4.0, 4.0, 9.0, 16.0])


def test_stitch_with_primary_y_axis():
    seg1 = ComputedSegment(
        X=np.array([0.0, 1.0, 4.0]),
        Y=np.array([0.0, 1.0, 2.0]),
    )
    seg2 = ComputedSegment(
        X=np.array([4.0, 9.0, 16.0]),
        Y=np.array([2.0 + 1e-9, 3.0, 4.0]),
    )

    stitched = stitch_segments([seg1, seg2], ["Y", "Y"], True, tol=1e-8)

    assert np.allclose(stitched.X, [0.0, 1.0, 4.0, 9.0, 16.0])
    assert np.allclose(stitched.Y, [0.0, 1.0, 2.0, 3.0, 4.0])
