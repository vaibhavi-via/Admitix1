export const NOTIFICATIONS_MODULE = {
  title: 'Notifications',
  endpoint: '/notifications',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const notificationsFields = [
  { name: "user_id", label: "User ID", type: "text", required: true , format: "uuid" },
  { name: "title", label: "Title", type: "text", required: true },
  { name: "message", label: "Message", type: "textarea", required: true },
  { name: "notification_type", label: "Type", type: "select", options: ["email", "sms", "in_app"] },
  { name: "is_read", label: "Read", type: "checkbox" }
]
