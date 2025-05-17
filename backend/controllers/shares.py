from fastapi import APIRouter, Depends, HTTPException
from service.shares import sharesService
from dtos.periodRequest import PeriodRequest

router = APIRouter(
    # prefix="/shares",
    # tags=["items"],
    # responses={404: {"description": "Not found"}},
)

@router.post('/getByPeriod')
async def get_shares_by_period(period: PeriodRequest):
    service = sharesService()

    if period.start_date > period.end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")

    shares = await service.getAllByPeriod(period.start_date, period.end_date)

    return shares