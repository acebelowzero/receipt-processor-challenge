from src.repo.base import RepoBase
from .model import Receipt


class ReceiptRepo(RepoBase[Receipt]):
    """Receipt Repo"""



receipt_repo = ReceiptRepo(Receipt)