from sqlalchemy import Boolean, Column, Integer, String, Date

# This is the line we changed.
# We are using a direct import 'from database' instead of a relative one 'from .database'
# This allows the seed.py script to run correctly.
from .database import Base

class Hiring(Base):
    __tablename__ = "hirings"

    id = Column(Integer, primary_key=True, index=True)
    business_group = Column(String, index=True)
    function = Column(String, index=True)
    role_title = Column(String)
    hire_date = Column(Date)
    cost_per_hire = Column(Integer)
    time_to_fill = Column(Integer)
    ijp_adherence = Column(Boolean)
    build_buy_ratio = Column(String)
    diversity_ratio = Column(Boolean)
    source = Column(String, index=True)

class BusinessSummary(Base):
    __tablename__ = "business_summaries"

    id = Column(Integer, primary_key=True, index=True)
    business_group = Column(String, index=True)
    function = Column(String, index=True)
    total_headcount = Column(Integer)
    available_headcount = Column(Integer)
    gap = Column(Integer)