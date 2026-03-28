from fastapi import APIRouter

from app.db.session import check_database_connection

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str | dict[str, str]]:
    db_ok, db_message = check_database_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "database": {
            "status": "ok" if db_ok else "error",
            "detail": db_message if not db_ok else "connected",
        },
    }
