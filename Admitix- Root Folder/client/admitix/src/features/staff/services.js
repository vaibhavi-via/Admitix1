import api from '../../api/axios'
const BASE_URL='/staff'
export function getStaffList(params){return api.get(BASE_URL,{params}).then(r=>r.data)}
export function getStaffById(id){return api.get(`${BASE_URL}/${id}`).then(r=>r.data)}
export function createStaff(payload){return api.post(BASE_URL,payload).then(r=>r.data)}
export function createStaffAccount(payload){return api.post(`${BASE_URL}/accounts`,payload).then(r=>r.data)}
export function updateStaff(id,payload){return api.patch(`${BASE_URL}/${id}`,payload).then(r=>r.data)}
export function deleteStaff(id){return api.delete(`${BASE_URL}/${id}`).then(r=>r.data)}
