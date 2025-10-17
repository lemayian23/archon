from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from . import Base

class AnalysisSession(Base):
    __tablename__ = \"analysis_sessions\"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_query = Column(Text)
    uploaded_filename = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default=\"processing\")
    
class AgentStep(Base):
    __tablename__ = \"agent_steps\"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    agent_type = Column(String)  # planner, coder, visualizer, critic
    input_data = Column(Text)
    output_data = Column(Text)
    code_generated = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AnalysisResult(Base):
    __tablename__ = \"analysis_results\"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    final_answer = Column(Text)
    visualization_code = Column(Text)
    data_summary = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
