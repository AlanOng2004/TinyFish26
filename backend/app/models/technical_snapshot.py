from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TechnicalSnapshot(Base):
    __tablename__ = "technical_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"), unique=True)
    short_ma: Mapped[float] = mapped_column(Float)
    long_ma: Mapped[float] = mapped_column(Float)
    rsi: Mapped[float] = mapped_column(Float)
    technical_label: Mapped[str] = mapped_column(String(32))

    run = relationship("Run", back_populates="technical_snapshot")
