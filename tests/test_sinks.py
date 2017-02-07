from .context import coldatoms
import numpy as np


class SinkPlane(coldatoms.Sink):
    pass


def test_CreateSinkPlane():
    sink = SinkPlane()
