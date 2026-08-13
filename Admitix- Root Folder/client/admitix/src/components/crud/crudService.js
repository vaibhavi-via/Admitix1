import api from '../../api/axios'

export function createCrudService(baseUrl) {
  return {
    list(params = {}) {
      return api.get(baseUrl, { params }).then((res) => res.data)
    },

    getById(id) {
      return api.get(`${baseUrl}/${id}`).then((res) => res.data)
    },

    create(payload) {
      return api.post(baseUrl, payload).then((res) => res.data)
    },

    update(id, payload) {
      return api.patch(`${baseUrl}/${id}`, payload).then((res) => res.data)
    },

    remove(id) {
      return api.delete(`${baseUrl}/${id}`).then((res) => res.data)
    },
  }
}