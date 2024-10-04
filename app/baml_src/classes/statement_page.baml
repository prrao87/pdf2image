// class Page {
//     page_number int @alias("id")
//     contains_transactions bool @alias("has_any_transaction_listed") @description(#"
//         Determines whether the bank statement page contains a list of transactions, can have one or more transactions.
//         Each transaction row is identified by date, description and amount.
//         Summary should be excluded.
//         Does not include checks or images of checks.
//     "#)
//     contains_account_summary bool @description("Determines whether the page contains account details information (business name, address, account number), not the name and address of a bank.")

// }

class PageHasTransactions {
    page_number int @alias("id")
    has_transactions bool @alias("has_any_transaction_listed") @description(#"
        Determines whether the bank statement page contains a list of transactions, can have one or more transactions.
        Each transaction row is identified by date, description and amount.
        Summary should be excluded.
        Does not include checks or images of checks.
    "#)
}

function CheckPageHasTransactions(statement_page: image) -> PageHasTransactions {
    client Sonnet
    prompt #"
        {{ _.role("user") }}
        Check whether the provided bank statement page contains a list of transactions.
        {{ statement_page }}
        {{ ctx.output_format }}
    "#
}