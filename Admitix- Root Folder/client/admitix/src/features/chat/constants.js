export const CHAT_MODULE = {
  title: 'Chat History',
  endpoint: '/chat-history',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const chatFields = [
  { name: "student_id", label: "Student", type: "select", required: true , format: "uuid", relation: "student" },
  { name: "question", label: "Question", type: "textarea", required: true },
  { name: "response", label: "Response", type: "textarea" }
]
