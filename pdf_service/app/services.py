import logging
import aioboto3
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet, StyleSheet1
from .core.config import settings
from .schemas import UserFromToken

logger = logging.getLogger(__name__)

class PDFService:
    """
    Service responsible for generating PDF documents using ReportLab.
    Encapsulates the document structure and styling logic.
    """

    def generate_pdf(self, user: UserFromToken) -> BytesIO:
        """Return a PDF stream containing the user profile."""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                title=f"Profile_{user.surname}",
                author="PDF Service"
            )

            styles = self._get_styles()
            story = self._build_story(user, styles)

            doc.build(story)
            buffer.seek(0)

            logger.info(f"PDF generated for user: {user.id}")
            return buffer

        except Exception as e:
            logger.error(f"PDF generation error for user {user.id}: {str(e)}", exc_info=True)
            raise RuntimeError(f"Could not build PDF: {e}")

    @staticmethod
    def _get_styles() -> StyleSheet1:
        """Provide stylesheet (can be extended with custom styles)."""
        try:
            return getSampleStyleSheet()
        except Exception as e:
            logger.error(f"Styles loading error: {e}")
            raise

    @staticmethod
    def _build_story(user: UserFromToken, styles: StyleSheet1) -> list[Flowable]:
        """Construct document flowables."""
        try:
            dob = (
                user.date_of_birth.strftime("%Y-%m-%d")
                if user.date_of_birth
                else "—"
            )

            return [
                Paragraph("User Profile Information", styles["Title"]),
                Spacer(1, 24),
                Paragraph(f"<b>Name:</b> {user.name}", styles["BodyText"]),
                Paragraph(f"<b>Surname:</b> {user.surname}", styles["BodyText"]),
                Paragraph(f"<b>Email:</b> {user.email}", styles["BodyText"]),
                Paragraph(f"<b>Date of Birth:</b> {dob}", styles["BodyText"]),
            ]
        except Exception as e:
            logger.error(f"Story building error for user {user.id}: {e}")
            raise



class QueueService:
    """
    Service for interacting with AWS SQS.
    """

    def __init__(self, session: aioboto3.Session):
        self.session = session
        self.endpoint_url = settings.AWS_ENDPOINT_URL
        self.region_name = settings.AWS_DEFAULT_REGION
        self.queue_name = settings.SQS_QUEUE_NAME

    async def _get_queue_url(self, sqs_client) -> str:
        """Retrieves the SQS Queue URL by its name."""
        response = await sqs_client.get_queue_url(QueueName=self.queue_name)
        return response["QueueUrl"]

    async def send_generate_task(self, user: UserFromToken):
        """Sends user data to the SQS queue for background processing."""
        try:
            async with self.session.client(
                    "sqs",
                    endpoint_url=self.endpoint_url,
                    region_name=self.region_name
            ) as sqs:
                queue_url = await self._get_queue_url(sqs)
                await sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=user.model_dump_json()
                )
                logger.info(f"Task for user {user.id} sent to SQS")
        except Exception as e:
            logger.error(f"Failed to send SQS message: {e}")
            raise e