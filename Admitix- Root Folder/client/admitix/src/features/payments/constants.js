export const PAYMENTS_MODULE = {
  title: 'Payments',
  endpoint: '/payments',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const paymentsFields = [
  { name: "application_id", label: "Application", type: "select", required: true , format: "uuid", relation: "application" },
  { name: "fee_id", label: "Fee Structure", type: "select", required: true , format: "uuid", relation: "fee" },
  { name: "amount_paid", label: "Amount Paid", type: "number", required: true },
  { name: "payment_mode", label: "Payment Mode", type: "select", options: ["online", "cash", "cheque", "dd", "card", "upi"] },
  { name: "transaction_id", label: "Transaction ID", type: "text" },
  { name: "payment_status", label: "Payment Status", type: "select", options: ["pending", "success", "failed", "refunded"] },
  { name: "payment_date", label: "Payment Date", type: "date" }
]
