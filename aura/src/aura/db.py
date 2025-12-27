from aura.features.memory import init_db
from aura.features.user_memory import init_user_memory


def init_aura_db():
    """
    Guaranteed DB + schema initializer.
    Safe to call multiple times.
    """
    init_db()
    init_user_memory()
