from logging import getLogger

from ingots.bootstrap.base import BaseBuilder

import ingot_grpclib as package

__all__ = ("IngotGrpclibBaseBuilder",)


logger = getLogger(__name__)


class IngotGrpclibBaseBuilder(BaseBuilder):

    package = package
