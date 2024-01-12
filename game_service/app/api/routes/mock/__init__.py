from .admin import router as admin_router
from .player import router as player_router
from .user import router as user_router
from .game import router as game_router
from .boat import router as boat_router
from .prize import router as prize_router

mock_routers = [
    user_router,
    admin_router,
    player_router,
    game_router,
    boat_router,
    prize_router
]
