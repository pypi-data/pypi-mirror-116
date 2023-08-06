import typing as t

from ingots.tests.units.bootstrap import test_base

from ingot_grpclib.bootstrap import IngotGrpclibBaseBuilder

__all__ = ("IngotGrpclibBaseBuilderTestCase",)


class IngotGrpclibBaseBuilderTestCase(test_base.BaseBuilderTestCase):
    """Contains tests for the IngotGrpclibBuilder class."""

    tst_cls: t.Type = IngotGrpclibBaseBuilder
    tst_entity_name: str = "ingot_grpclib"
    tst_entity_name_upper: str = "INGOT_GRPCLIB"
    tst_entity_name_class_name: str = "IngotGrpclib"
    tst_entity_description = "Provides gRPC functionality based on the grpclib package"
