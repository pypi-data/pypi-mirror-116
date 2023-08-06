import typing as t

from ingots.tests.units.scripts import test_base

from ingot_grpclib.scripts.ingot_grpclib import IngotGrpclibDispatcher

__all__ = ("IngotGrpclibDispatcherTestCase",)


class IngotGrpclibDispatcherTestCase(test_base.BaseDispatcherTestCase):
    """Contains tests for the IngotGrpclibDispatcher class and checks it."""

    tst_cls: t.Type = IngotGrpclibDispatcher
    tst_builder_name = "test"
