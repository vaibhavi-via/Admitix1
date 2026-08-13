export const ENTRANCE_EXAM_SCORES_MODULE = {
  title: 'Entrance Exam Scores',
  endpoint: '/entrance-exam-scores',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const entranceExamScoresFields = [
  { name: "student_id", label: "Student", type: "select", required: true , format: "uuid", relation: "student" },
  { name: "exam_name", label: "Exam Name", type: "text", required: true },
  { name: "roll_number", label: "Roll Number", type: "text" },
  { name: "score", label: "Score", type: "number" },
  { name: "percentile", label: "Percentile", type: "number" },
  { name: "rank", label: "Rank", type: "number" },
  { name: "exam_year", label: "Exam Year", type: "number" }
]
