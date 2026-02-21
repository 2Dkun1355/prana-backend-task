import asyncio
import json
import logging
import aioboto3
from .services import PDFService
from .schemas import UserFromToken
from .core.config import settings

logger = logging.getLogger(__name__)


class PDFWorker:
    """
    Background worker that consumes messages from SQS, generates PDF documents,
    and uploads them to an S3 bucket.
    """

    def __init__(self):
        self.session = aioboto3.Session()
        self.pdf_service = PDFService()

        self.endpoint_url = settings.AWS_ENDPOINT_URL
        self.region_name = settings.AWS_DEFAULT_REGION
        self.queue_name = settings.SQS_QUEUE_NAME
        self.bucket_name = settings.S3_BUCKET_NAME

    async def _init_resources(self, sqs, s3):
        """
        Ensures that the required SQS queue and S3 bucket exist.
        Commonly used for local development with Localstack.
        """
        logger.info(f"Checking resources: Queue='{self.queue_name}', Bucket='{self.bucket_name}'")
        await sqs.create_queue(QueueName=self.queue_name)
        try:
            await s3.create_bucket(Bucket=self.bucket_name)
        except Exception:
            pass

    async def process_message(self, msg, s3) -> None:
        """
        Parses the SQS message, triggers PDF generation, and stores the result in S3.
        """
        try:
            body = json.loads(msg["Body"])
            user = UserFromToken(**body)

            logger.info(f"Generating PDF for user: {user.email}")
            pdf_buffer = self.pdf_service.generate_pdf(user)

            file_name = f"profile_{user.id}.pdf"
            await s3.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=pdf_buffer.getvalue(),
                ContentType="application/pdf"
            )
            logger.info(f"Successfully uploaded {file_name} to S3")

        except Exception as e:
            logger.error(f"Failed to process message: {e}", exc_info=True)
            raise

    async def run(self):
        """
        Starts the worker's main loop to poll messages from the SQS queue.
        """
        async with self.session.client("sqs", endpoint_url=self.endpoint_url, region_name=self.region_name) as sqs, \
                self.session.client("s3", endpoint_url=self.endpoint_url, region_name=self.region_name) as s3:

            await self._init_resources(sqs, s3)

            queue_data = await sqs.get_queue_url(QueueName=self.queue_name)
            queue_url = queue_data['QueueUrl']

            logger.info(f"PDF Worker is running. Polling: {queue_url}")

            while True:
                try:
                    response = await sqs.receive_message(
                        QueueUrl=queue_url,
                        WaitTimeSeconds=10,
                        MaxNumberOfMessages=1
                    )

                    if "Messages" not in response:
                        continue

                    for msg in response["Messages"]:
                        await self.process_message(msg, s3)

                        await sqs.delete_message(
                            QueueUrl=queue_url,
                            ReceiptHandle=msg["ReceiptHandle"]
                        )

                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    await asyncio.sleep(5)


if __name__ == "__main__":
    worker = PDFWorker()
    try:
        asyncio.run(worker.run())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
