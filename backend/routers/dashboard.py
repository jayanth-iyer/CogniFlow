from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from database import get_session
from models.seller import Seller
from models.document import Document

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(session: Session = Depends(get_session)):
    """
    Get aggregated statistics for the dashboard.
    """
    total_sellers = session.exec(select(func.count(Seller.id))).one()
    pending_documents = session.exec(select(func.count(Document.id)).where(Document.status == "pending")).one()
    
    # For "AI Request Rate", we don't have a real metric yet (no analytics table),
    # so we'll mock it or calculate something simple like "total documents" as a proxy for activity for now.
    # In a real app, this would query a 'request_logs' table.
    # Let's return total_documents for now as "AI Activity base"
    total_documents = session.exec(select(func.count(Document.id))).one()
    
    return {
        "total_sellers": total_sellers,
        "pending_documents": pending_documents,
        "ai_request_rate": total_documents * 5 + 120 # Mocking a rate based on activity
    }
