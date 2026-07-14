"""
Smoke tests.
"""


def test_project_modules_import():
    """
    Main project modules should import without errors.
    """

    from src.core import router
    from src.core import session

    from src.database import repositories
    from src.database import statistics_repository

    from src.services import database_service
    from src.services import image_quality_service

    from src.game.belote import scoring

    assert router is not None
    assert session is not None
    assert repositories is not None
    assert statistics_repository is not None
    assert database_service is not None
    assert image_quality_service is not None
    assert scoring is not None