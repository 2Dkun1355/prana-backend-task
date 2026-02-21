from fastapi import APIRouter, Response, HTTPException, status
from .dependencies import CurrentUserDepends, PDFServiceDepends, QueueServiceDepends

pdf_router = APIRouter(prefix="/api/pdf", tags=["PDF"])


@pdf_router.get(
    "/download",
    response_class=Response,
    status_code=status.HTTP_200_OK,
)
async def download_pdf(
        current_user: CurrentUserDepends,
        pdf_service: PDFServiceDepends
):
    """
    Generates and returns the current user's profile as a PDF file.
    """
    try:
        pdf_buffer = pdf_service.generate_pdf(user=current_user)

        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=profile_{current_user.id}.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Generation Error",
                "message": "An unexpected error occurred while assembling the PDF document.",
                "code": "PDF_GEN_FAILED"
            }
        )


@pdf_router.post(
    "/upload-to-s3",
    status_code=status.HTTP_202_ACCEPTED,
)
async def s3_upload_pdf(
        current_user: CurrentUserDepends,
        queue_service: QueueServiceDepends
):
    """
    Triggers an asynchronous task to generate and upload the user's PDF to S3.
    """
    try:
        await queue_service.send_generate_task(current_user)
        return {
            "status": "accepted",
            "user_id": current_user.id,
            "message": "Task queued successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Queue Service Error",
                "message": "We are unable to process your request at the moment. Please try again later.",
                "code": "QUEUE_UNAVAILABLE"
            }
        )