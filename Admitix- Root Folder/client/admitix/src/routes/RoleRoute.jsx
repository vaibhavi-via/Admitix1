
import {Navigate,Outlet} from 'react-router-dom'
import {useAuth} from '../context/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'
export function RoleRoute({roles=[]}){const{user,isLoading,isAuthenticated}=useAuth();if(isLoading)return <LoadingSpinner fullScreen label="Loading your workspace…"/>;if(!isAuthenticated)return <Navigate to="/login" replace/>;return roles.includes(user?.role_name)?<Outlet/>:<Navigate to={user?.role_name==='student'?'/student':user?.role_name?.includes('officer')?'/officer':'/dashboard'} replace/>}
export function RoleLanding(){const{user,isLoading}=useAuth();if(isLoading)return <LoadingSpinner fullScreen label="Loading your workspace…"/>;const r=user?.role_name;if(r==='student')return <Navigate to="/student" replace/>;if(r==='admission_officer'||r==='department_reviewer')return <Navigate to="/officer" replace/>;return <Navigate to="/dashboard" replace/>}
