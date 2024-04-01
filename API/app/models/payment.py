from app.models import Base
from app.models.user import BaseModel
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Date, Enum
from app.utils.helper import send_attachment
from os import getenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


class Payment(BaseModel, Base):
    """The Payment model."""

    __tablename__ = "payments"
    amount = Column(Integer, nullable=False)
    card_type = Column(Enum("Visa", "Master Card"))
    card_owner = Column(String(100), nullable=False)
    card_number = Column(String(16), nullable=False)
    card_cvv = Column(String(3), nullable=False)
    card_expiry_date = Column(Date, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    premium_account_id = Column(
        String(60), ForeignKey("premium_accounts.id"), nullable=False
    )

    def generate_invoice(self, data, firstName, lastName, email):
        """A method that generates the payment history."""
        path = getenv("PWD")
        subject = "Booker payment invoice."
        filename = f"{path}/app/templates/attachments/invoice.pdf"
        document = SimpleDocTemplate(filename, pagesize=letter)
        data_table = [["Payment date", "Card owner", "Payment amount"]]
        for item in data:
            data_table.append([item["created_at"], item["card_owner"], item["amount"]])

        table = Table(data_table)
        table.setStyle(
            TableStyle(
                [
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.gray),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        header_text = f"BOOKER invoice for {firstName} {lastName}"
        styles = getSampleStyleSheet()
        header_style = styles["Heading1"]
        header = Paragraph(header_text, header_style)
        elements = [header, table]
        document.build(elements)
        send_attachment(firstName, email, filename, subject)
