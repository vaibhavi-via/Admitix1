import api from '../../api/axios'

// All AI Verification API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/ai-verifications'

export function getAiVerificationList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getAiVerificationById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createAiVerification(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateAiVerification(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteAiVerification(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}

export const verifyAndPersistDocument=(id,file)=>{const f=new FormData();f.append('file',file);return api.post(`/ai/document-verification/${id}`,f,{headers:{'Content-Type':'multipart/form-data'}}).then(r=>r.data)}
