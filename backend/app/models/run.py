from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(16), index=True)
    run_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    technical_score: Mapped[float] = mapped_column(Float)
    sentiment_score: Mapped[float] = mapped_column(Float)
    historical_score: Mapped[float] = mapped_column(Float)
    discrepancy_score: Mapped[float] = mapped_column(Float)
    stance: Mapped[str] = mapped_column(String(32))
    confidence: Mapped[float] = mapped_column(Float)
    memo_thesis: Mapped[str] = mapped_column(Text)
    memo_technical_view: Mapped[str] = mapped_column(Text)
    memo_news_view: Mapped[str] = mapped_column(Text)
    memo_historical_view: Mapped[str] = mapped_column(Text)
    memo_risks: Mapped[str] = mapped_column(Text)
    memo_final_verdict: Mapped[str] = mapped_column(Text)

    articles = relationship("Article", back_populates="run", cascade="all, delete-orphan")
    technical_snapshot = relationship(
        "TechnicalSnapshot",
        back_populates="run",
        cascade="all, delete-orphan",
        uselist=False,
    )
    historical_assessment = relationship(
        "HistoricalAssessment",
        back_populates="run",
        cascade="all, delete-orphan",
        uselist=False,
    )
