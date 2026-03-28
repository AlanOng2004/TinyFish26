from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class HistoricalAssessment(Base):
    __tablename__ = "historical_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), unique=True)
    matched_pattern: Mapped[str] = mapped_column(String(128))
    historical_label: Mapped[str] = mapped_column(String(32))
    rationale: Mapped[str] = mapped_column(Text)
    pattern_score: Mapped[float] = mapped_column(Float)

    run = relationship("Run", back_populates="historical_assessment")
