"""
Health check route module.
"""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """Health check endpoint to verify backend status."""
    return {
        "status": "healthy",
        "service": "Student Internship & Job Opportunity Platform API",
        "version": "1.0.0",
    }
