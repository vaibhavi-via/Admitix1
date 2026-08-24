
import {useEffect,useState} from 'react'
import {useAuth} from '../../../context/AuthContext'
import {getStudent,updateStudent} from './api'
import {Card,Button,Field,Loading,ErrorBox} from '../components/PortalUI'
export default function StudentProfilePage(){
 const {user}=useAuth();const [form,setForm]=useState({});const[loading,setLoading]=useState(true);const[saving,setSaving]=useState(false);const[error,setError]=useState('');const[ok,setOk]=useState('')
 useEffect(()=>{getStudent(user.student_id).then(setForm).catch(e=>setError(e.message)).finally(()=>setLoading(false))},[user.student_id])
 const set=(k,v)=>setForm(x=>({...x,[k]:v}))
 if(loading)return <Loading/>
 return <div className="max-w-4xl space-y-5"><div><h2 className="text-xl font-bold">My Profile</h2><p className="mt-1 text-sm text-slate-500">Keep your personal and contact information accurate.</p></div><ErrorBox message={error}/>{ok&&<div className="rounded-xl bg-emerald-50 p-3 text-sm text-emerald-700">{ok}</div>}
 <Card><div className="grid gap-4 md:grid-cols-2">
 {['aadhaar_no','dob','blood_group','category','nationality','address','city','state','pincode','parent_name','parent_phone','guardian_email'].map(k=><Field key={k} label={k.replaceAll('_',' ')} value={form[k]||''} onChange={e=>set(k,k==='dob'?e.target.value:e.target.value)} type={k==='dob'?'date':k.includes('phone')?'tel':k.includes('email')?'email':'text'} className={k==='address'?'md:col-span-2':''}/>)}
 </div><div className="mt-5"><Button disabled={saving} onClick={async()=>{setSaving(true);setError('');setOk('');try{await updateStudent(user.student_id,form);setOk('Profile updated successfully.')}catch(e){setError(e.message)}finally{setSaving(false)}}}>{saving?'Saving...':'Save Profile'}</Button></div></Card></div>
}
