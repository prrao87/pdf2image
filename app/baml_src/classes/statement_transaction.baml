class Transaction {
  date string @alias("transaction_date")
  description string | null @alias("transaction_description")
  amount float @alias("transaction_amount")
  transaction_type TransactionType
}

enum TransactionType {
  Deposit @description("Deposit or addition")
  Withdrawal @description("Withdrawal or deduction")
  Other @description("Other type of transaction like a fee, charge, etc.")
}

function ExtractStatementPageTransactions(statement_page: image) -> Transaction[] {
  client Sonnet
  prompt #"
    {{ _.role("user") }}
    Scan and extract all the transaction items from the provided bank statement page.
    Each transaction row is identified by date, description and amount.
    Do not mix transactions with other types of information like summaries or checks.
    Try not to miss any.
    {{ statement_page }}
    {{ ctx.output_format }}
  "#
}
 
function Hi(input: string) -> string {
  client Sonnet
  prompt #"
    TCouun
    {{ _.role("user") }}
    Hi {{ input}} 

  "#
}
