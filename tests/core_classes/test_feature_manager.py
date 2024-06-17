from unittest.mock import MagicMock
from MeatuchuRPGMapMaker.core_classes import FeatureManager


def test_build_singletons() -> None:
    class TestFeatureManager(FeatureManager):
        def __build__(self) -> None:
            pass

    TestFeatureManager.__build__ = MagicMock()
    TestFeatureManager()
    TestFeatureManager()
    TestFeatureManager.__build__.assert_called_once()
