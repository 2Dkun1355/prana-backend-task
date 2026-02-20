from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.schemas import UserFromToken


class PDFService:
    """
    Service responsible for generating PDF documents using ReportLab.
    Encapsulates the document structure and styling logic.
    """

    def generate_pdf(self, user: UserFromToken) -> BytesIO:
        """
        Creates a PDF profile document in memory.

        Args:
            user: User data validated by UserFromToken schema.

        Returns:
            BytesIO: A binary stream containing the generated PDF.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            title=f"Profile_{user.last_name}",
            author="PDF Service"
        )

        styles = getSampleStyleSheet()

        story = [
            Paragraph("User Profile Information", styles["Title"]),
            Spacer(1, 24),
            Paragraph(f"<b>First Name:</b> {user.first_name}", styles["BodyText"]),
            Paragraph(f"<b>Last Name:</b> {user.last_name}", styles["BodyText"]),
            Paragraph(f"<b>Email:</b> {user.email}", styles["BodyText"]),
            Paragraph(f"<b>Date of Birth:</b> {user.date_of_birth.strftime('%Y-%m-%d')}", styles["BodyText"]),
        ]

        doc.build(story)
        buffer.seek(0)
        return buffer