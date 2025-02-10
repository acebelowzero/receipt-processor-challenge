from src.repo.base import RepoBase

from .model import Point


class PointRepo(RepoBase[Point]):
    """Point Repo"""



point_repo = PointRepo(Point)