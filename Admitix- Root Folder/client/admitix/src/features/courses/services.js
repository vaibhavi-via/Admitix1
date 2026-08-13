import api from '../../api/axios'

// All Courses API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/courses'

export function getCoursesList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getCoursesById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createCourse(payload) {
    const { department_id, institution_id, course_name, course_code, duration_years, eligibility, status } = payload
  return api.post(BASE_URL, { department_id, institution_id, course_name, course_code, duration_years, eligibility, status }).then((res) => res.data)
}

export function updateCourse(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteCourse(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
