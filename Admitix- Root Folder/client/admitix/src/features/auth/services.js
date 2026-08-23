import api from '../../api/axios'
export const registerRequest=(payload)=>api.post('/auth/register',payload).then(r=>r.data)
export const loginRequest=(payload)=>api.post('/auth/login',payload).then(r=>r.data)
export const refreshTokenRequest=(refresh_token)=>api.post('/auth/refresh-token',{refresh_token}).then(r=>r.data)
export const logoutRequest=()=>api.post('/auth/logout').then(r=>r.data)
export const getCurrentUser=()=>api.get('/auth/me').then(r=>r.data)
export const changePasswordRequest=(payload)=>api.post('/auth/change-password',payload).then(r=>r.data)
