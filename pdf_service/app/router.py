from fastapi import APIRouter, Response
from app.dependencies import CurrentUserDepends, PDFServiceDepends

pdf_router = APIRouter(prefix="/api/pdf", tags=["PDF"])

@pdf_router.get("/download")
async def download_pdf(
    current_user: CurrentUserDepends,
    pdf_service: PDFServiceDepends
) -> Response:
    """
    Generates and returns a PDF document containing the user's profile data.
    Requires a valid Bearer token for authentication.
    """
    pdf_buffer = pdf_service.generate_pdf(user=current_user)

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=profile_{current_user.id}.pdf",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )