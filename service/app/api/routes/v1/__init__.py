from .auth import router as auth_router
from .user import router as user_router
from .player import router as player_router

v1_routers = [
    auth_router,
    user_router,
    player_router,
]
