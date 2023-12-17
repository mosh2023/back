from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import Response
from medsi_fastapi.generic.probs_schema import ProbItem
from medsi_fastapi.probs import ProbesConstructor

from app.core.logging import logger


router = APIRouter()


def get_probes_constructor() -> ProbesConstructor:
    pc = ProbesConstructor(logger=logger)

    return pc


@router.get(
    "/live",
    name="service:live",
)
async def get_live():
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/ready",
    name="service:ready",
    response_model=List[ProbItem],
)
async def get_ready(response: Response):
    pc = get_probes_constructor()
    prob_data = await pc.get_data()
    response.status_code = (
        status.HTTP_200_OK if pc.is_alive() else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return prob_data


@router.get(
    "/healthcheck",
    name="service:healthcheck",
    response_model=List[ProbItem],
)
async def get_healthcheck():
    pc = get_probes_constructor()
    prob_data = await pc.get_data()
    return prob_data


@router.get(
    "/exception",
    name="service:exception",
)
async def get_exception():
    raise ValueError("Just an exception check")
