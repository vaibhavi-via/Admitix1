import api from '../../api/axios'

// All Entrance Exam Scores API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/entrance-exam-scores'

export function getEntranceExamScoresList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getEntranceExamScoresById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createEntranceExamScore(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateEntranceExamScore(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteEntranceExamScore(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
