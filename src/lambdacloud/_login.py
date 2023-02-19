import os
from pathlib import Path
from typing import Optional

from .constants import LAMBDA_TOKEN_PATH


class LambdaFolder:
    path_token = Path(LAMBDA_TOKEN_PATH)

    @classmethod
    def save_token(cls, token: str) -> None:
        """
        Save token, creating folder as needed.

        Token is saved in the lambda home folder. You can configure it by setting
        the `LAMBDA_HOME` environment variable.

        Args:
            token (`str`):
                The token to save to the [`LambdaFolder`]
        """
        cls.path_token.parent.mkdir(parents=True, exist_ok=True)
        cls.path_token.write_text(token)

    @classmethod
    def get_token(cls) -> Optional[str]:
        """
        Get token or None if not existent.

        Note that a token can be also provided using the `LAMBDA_TOKEN` environment variable.

        Token is saved in the lambda home folder. You can configure it by setting
        the `LAMBDA_HOME` environment variable. Previous location was `~/.lambda/token`.

        Returns:
            `str` or `None`: The token, `None` if it doesn't exist.
        """
        # 1. Is it set by environment variable ?
        token: Optional[str] = os.environ.get("LAMBDA_TOKEN")
        if token is not None:
            return token

        # 2. Is it set in token path ?
        try:
            return cls.path_token.read_text()
        except FileNotFoundError:
            return None

    @classmethod
    def delete_token(cls) -> None:
        """
        Deletes the token from storage. Does not fail if token does not exist.
        """
        try:
            cls.path_token.unlink()
        except FileNotFoundError:
            pass


def login(token: str) -> None:
    """
    Save token to local storage.

    Args:
        token (`str`):
            The token to save to the [`LambdaFolder`]
    """
    LambdaFolder.save_token(token)
