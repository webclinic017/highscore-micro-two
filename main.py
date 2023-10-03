from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.sessions import SessionMiddleware

from core.config import starlette_config
from core.db import DBSetup
from core.models import HighScore, HighScoreCreate

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=starlette_config.get('SECRET_KEY'))
db_setup = DBSetup()


@app.get("/high_scores")
async def get_high_scores():
    session = await db_setup.get_session()
    result = await session.execute(select(HighScore))
    high_scores = result.scalars().all()
    return [HighScore(initials=hs.initials, score=hs.score) for hs in high_scores]


@app.put("/add_score")
async def add_score_to_list(high_score: HighScoreCreate,
                            session: AsyncSession = Depends(db_setup.get_session)):
    """ Add a new score with initials to a list of high scores,
    sort the list in descending order, and keep only the top 10
    scores in the database.
    Inputs:
    - initials: a string representing the initials of the player who achieved the score.
    - score: an integer representing the score achieved by the player. """
    hs = HighScore(initials=high_score.initials[:3].upper(),
                   score=high_score.score)
    session.add(hs)
    await session.commit()
    await session.refresh()
    return hs


@app.post("/clear_scores")
async def clear_high_score_list(session: AsyncSession = Depends(db_setup.get_session)):
    session.delete(HighScore)
    session.flush()
