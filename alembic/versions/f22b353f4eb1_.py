"""empty message

Revision ID: f22b353f4eb1
Revises: 2c44261f2c30
Create Date: 2025-06-28 15:03:43.114437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f22b353f4eb1'
down_revision: Union[str, Sequence[str], None] = '2c44261f2c30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
