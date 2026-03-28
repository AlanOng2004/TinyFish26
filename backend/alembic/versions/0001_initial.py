"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-03-28 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ticker", sa.String(length=16), nullable=False),
        sa.Column("run_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("technical_score", sa.Float(), nullable=False),
        sa.Column("sentiment_score", sa.Float(), nullable=False),
        sa.Column("historical_score", sa.Float(), nullable=False),
        sa.Column("discrepancy_score", sa.Float(), nullable=False),
        sa.Column("stance", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("memo_thesis", sa.Text(), nullable=False),
        sa.Column("memo_technical_view", sa.Text(), nullable=False),
        sa.Column("memo_news_view", sa.Text(), nullable=False),
        sa.Column("memo_historical_view", sa.Text(), nullable=False),
        sa.Column("memo_risks", sa.Text(), nullable=False),
        sa.Column("memo_final_verdict", sa.Text(), nullable=False),
    )
    op.create_index("ix_runs_id", "runs", ["id"])
    op.create_index("ix_runs_ticker", "runs", ["ticker"])
    op.create_index("ix_runs_run_timestamp", "runs", ["run_timestamp"])

    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("sentiment", sa.String(length=32), nullable=False),
        sa.Column("relevance_score", sa.Float(), nullable=False),
        sa.Column("catalyst_type", sa.String(length=64), nullable=False),
    )
    op.create_index("ix_articles_id", "articles", ["id"])

    op.create_table(
        "technical_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("runs.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("short_ma", sa.Float(), nullable=False),
        sa.Column("long_ma", sa.Float(), nullable=False),
        sa.Column("rsi", sa.Float(), nullable=False),
        sa.Column("technical_label", sa.String(length=32), nullable=False),
    )
    op.create_index("ix_technical_snapshots_id", "technical_snapshots", ["id"])

    op.create_table(
        "historical_assessments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("runs.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("matched_pattern", sa.String(length=128), nullable=False),
        sa.Column("historical_label", sa.String(length=32), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("pattern_score", sa.Float(), nullable=False),
    )
    op.create_index("ix_historical_assessments_id", "historical_assessments", ["id"])


def downgrade() -> None:
    op.drop_index("ix_historical_assessments_id", table_name="historical_assessments")
    op.drop_table("historical_assessments")
    op.drop_index("ix_technical_snapshots_id", table_name="technical_snapshots")
    op.drop_table("technical_snapshots")
    op.drop_index("ix_articles_id", table_name="articles")
    op.drop_table("articles")
    op.drop_index("ix_runs_run_timestamp", table_name="runs")
    op.drop_index("ix_runs_ticker", table_name="runs")
    op.drop_index("ix_runs_id", table_name="runs")
    op.drop_table("runs")
