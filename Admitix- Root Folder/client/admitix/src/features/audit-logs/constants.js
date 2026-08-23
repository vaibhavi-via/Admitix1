export const AUDIT_LOGS_MODULE = {
  title: 'Audit Logs',
  endpoint: '/audit-logs',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const auditLogsFields = [
  { name: "user_id", label: "User ID", type: "text" , format: "uuid" },
  { name: "institution_id", label: "Institution ID", type: "text" , format: "uuid" },
  { name: "action", label: "Action", type: "text", required: true },
  { name: "table_name", label: "Table Name", type: "text", required: true },
  { name: "record_id", label: "Record ID", type: "text" , format: "uuid" },
  { name: "ip_address", label: "IP Address", type: "text" }
]
