from app.baml_client import b
from app.baml_client.types import TransactionType
from baml_py import Image
from app.util.pdf import pdf_to_image_base64
import os
from fastapi import UploadFile
import pytest


@pytest.mark.asyncio
async def test_extract_text_from_pdf():
    pdf_path = "tests/files/test.pdf"
    with open(pdf_path, "rb") as file:
        pdf_file = UploadFile(file, filename=os.path.basename(pdf_path))
        statement_pages = [
            Image.from_base64(media_type="image/png", base64=imageb64string)
            for imageb64string in pdf_to_image_base64(pdf_file)
        ]

    transactions = []

    for page_image_index, page_image in enumerate(statement_pages):
        page_parsed = b.CheckPageHasTransactions(page_image)
        if page_parsed.has_transactions:
            transactions.extend(
                b.ExtractStatementPageTransactions(statement_pages[page_image_index])
            )

    print(transactions)
    print("Extracted transactions:")
    total_withdrawals = 0
    total_deposits = 0

    for transaction in transactions:
        if transaction.transaction_type == TransactionType.Withdrawal:
            total_withdrawals += transaction.amount
            print(f"    Withdrawal: {transaction.amount:.2f}")
        elif transaction.transaction_type == TransactionType.Deposit:
            total_deposits += transaction.amount
            print(f"    Deposit: {transaction.amount:.2f}")
        else:
            print(f"    Other: {transaction.amount:.2f}")

    remaining_balance = total_deposits - total_withdrawals

    print(f"Total withdrawals: {total_withdrawals:.2f}")
    print(f"Total deposits: {total_deposits:.2f}")
    print(f"Remaining balance: {remaining_balance:.2f}")


amounts = [
    "$1,453.80-",
    "$270.03-",
    "$552.59-",
    "$564.99-",
    "$302.91-",
    "$300.00-",
    "$82.79-",
    "$644.98-",
    "$1,710.50-",
    "$613.57-",
    "$336.75-",
    "$340.88-",
    "$3421.45-",
    "$4.00-",
    "$4.00-",
    "$13.50-",
    "$541.20-",
    "$503.55-",
    "$550.01-",
    "$201.74-",
    "$120.00-",
    "$135.53-",
    "$283.06-",
    "$286.97-",
    "$55.00-",
    "13.50-",
    "220.60-",
    "300.15-",
    "310.84-",
    "461.17-",
    "471.09-",
    "585.53-",
    "261.64-",
    "275.21-",
    "1,050.00-",
    "1,918.00-",
    "10,000.00-",
    "498.38-",
    "2.00-",
    "229.36-",
    "2,100.00-",
    "612.46-",
    "44.57-",
    "268.25-",
    "433.29-",
    "159.67-",
    "13.50-",
    "349.11-",
    "407.22-",
    "159.59-",
    "282.41-",
    "365.13-",
    "369.73-",
    "447.40-",
    "322.40-",
    "18.13-",
    "272.70-",
    "1,042.24-",
    "270.95-",
    "305.23-",
    "420.83-",
    "288.16",
    "662.02",
    "1,420.10",
    "3,553.50",
    "16.50-",
    "5,000.00-",
    "211.21-",
    "464.09-",
]


# @pytest.mark.asyncio
def test_calculate_total_amount():
    parse_amount = lambda amount_str: float(
        amount_str.replace("$", "").replace(",", "").replace("-", "")
    )
    total = sum(parse_amount(amount) for amount in amounts)
    assert (
        round(total, 2) == 34334.72
    ), f"Expected total to be 34334.72, but got {total}"
    print(f"Total amount calculated: {total}")
