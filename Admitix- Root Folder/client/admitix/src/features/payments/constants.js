export const PAYMENTS_MODULE = {
  title: 'Payments',
  endpoint: '/payments',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const paymentsFields = [
  { name: "application_id", label: "Application ID", type: "text", required: true , format: "uuid" },
  { name: "fee_id", label: "Fee Structure ID", type: "text", required: true , format: "uuid" },
  { name: "amount_paid", label: "Amount Paid", type: "number", required: true },
  { name: "payment_mode", label: "Payment Mode", type: "select", options: ["online", "cash", "cheque", "dd", "card", "upi"] },
  { name: "transaction_id", label: "Transaction ID", type: "text" },
  { name: "payment_status", label: "Payment Status", type: "select", options: ["pending", "success", "failed", "refunded"] },
  { name: "payment_date", label: "Payment Date", type: "date" }
]
