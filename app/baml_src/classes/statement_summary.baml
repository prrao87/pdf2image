
class FinancialSummary {
  bank_name string
  business_name string
  business_account_number string
  business_address string
  beginning_balance float @alias("beginning_balance_gaap_format")
  ending_balances EndingBalanceItem[] @alias("ending_balances_per_day")
  // deposits DepositsItem[] @alias("deposits_and_additions")
  // withdrawals WithdrawalsItem[]
  // fees FeesItem[]
}

class EndingBalanceItem {
  date string @alias("date_of_ending_balance")
  amount float @alias("ending_balance_amount")
}
 
function ExtractFinancialSummaryData(statements: image[] | string[]) -> FinancialSummary {
  client Sonnet
  prompt #"
    {# start a user message #}
    {{ _.role("user") }}

    Scan and extract the financial data from all pages of this bank statement.
    {{ statements }}

    {# special macro to print the output schema instructions. #}
    {{ ctx.output_format }}
  "#
}
