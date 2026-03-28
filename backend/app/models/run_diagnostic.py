from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class RunDiagnostic(Base):
    __tablename__ = "run_diagnostics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), unique=True)
    source_success_count: Mapped[int] = mapped_column(Integer, default=0)
    source_failure_count: Mapped[int] = mapped_column(Integer, default=0)
    price_point_count: Mapped[int] = mapped_column(Integer, default=0)
    technical_data_quality: Mapped[str] = mapped_column(String(32), default="limited")
    sentiment_mode: Mapped[str] = mapped_column(String(32), default="heuristic")
    memo_mode: Mapped[str] = mapped_column(String(32), default="template")
    fallback_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    run = relationship("Run", back_populates="diagnostic")
