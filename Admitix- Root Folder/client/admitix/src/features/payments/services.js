import api from '../../api/axios'

// All Payments API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/payments'

export function getPaymentsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getPaymentsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createPayment(payload) {
    const { application_id, fee_id, amount_paid, payment_mode, transaction_id } = payload
  return api.post(BASE_URL, { application_id, fee_id, amount_paid, payment_mode, transaction_id }).then((res) => res.data)
}

export function updatePayment(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deletePayment(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
