import {Navigate,Outlet} from 'react-router-dom'
import {useAuth} from '../context/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'

export function RoleRoute({roles=[]}){
 const{user,isLoading,isAuthenticated}=useAuth()
 if(isLoading)return <LoadingSpinner fullScreen label="Loading your workspace…"/>
 if(!isAuthenticated)return <Navigate to="/login" replace/>
 if(roles.includes(user?.role_name))return <Outlet/>
 if(user?.role_name==='student')return <Navigate to="/student" replace/>
 if(user?.role_name==='admission_officer'||user?.role_name==='department_reviewer')return <Navigate to="/officer" replace/>
 return <Navigate to="/" replace/>
}

export function RoleLanding(){
 const{user,isLoading}=useAuth()
 if(isLoading)return <LoadingSpinner fullScreen label="Loading your workspace…"/>
 const r=user?.role_name
 if(r==='student')return <Navigate to="/student" replace/>
 if(r==='admission_officer'||r==='department_reviewer')return <Navigate to="/officer" replace/>
 if(r==='super_admin'||r==='institution_admin')return <Navigate to="/dashboard" replace/>
 return <Navigate to="/login" replace/>
}
