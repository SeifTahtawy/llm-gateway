from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/api/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


def check_ci() -> int:
    return "hello"
