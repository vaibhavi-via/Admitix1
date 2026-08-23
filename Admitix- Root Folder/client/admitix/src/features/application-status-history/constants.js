export const APPLICATION_STATUS_HISTORY_MODULE = {
  title: 'Application Status History',
  endpoint: '/application-status-history',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const applicationStatusHistoryFields = [
  { name: "application_id", label: "Application ID", type: "text", required: true , format: "uuid" },
  { name: "old_status", label: "Old Status", type: "text" },
  { name: "new_status", label: "New Status", type: "text", required: true },
  { name: "changed_by", label: "Changed By (User ID)", type: "text" , format: "uuid" },
  { name: "remarks", label: "Remarks", type: "textarea" }
]
