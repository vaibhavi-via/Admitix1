
import {useEffect,useState} from 'react'
import {useAuth} from '../../../context/AuthContext'
import {useNavigate} from 'react-router-dom'
import {FileText,Upload,CheckCircle2,Clock,ArrowRight} from 'lucide-react'
import {getApplications,getDocuments} from './api'
import {Card,Badge,Loading,ErrorBox} from '../components/PortalUI'
export default function StudentDashboardPage(){
 const {user}=useAuth(); const nav=useNavigate(); const [apps,setApps]=useState([]); const [docs,setDocs]=useState([]); const [error,setError]=useState(''); const [loading,setLoading]=useState(true)
 useEffect(()=>{Promise.all([getApplications(),getApplications().then(async a=>a[0]?getDocuments(a[0].application_id):[]) ]).then(([a,d])=>{setApps(a||[]);setDocs(d||[])}).catch(e=>setError(e.message)).finally(()=>setLoading(false))},[])
 if(loading)return <Loading/>
 const app=apps[0]; const verified=docs.filter(d=>d.verification_status==='verified').length
 return <div className="space-y-6">
  <ErrorBox message={error}/>
  <div className="rounded-2xl bg-gradient-to-br from-emerald-700 via-emerald-600 to-green-500 p-6 text-white shadow-lg sm:p-8">
   <p className="text-xs font-semibold uppercase tracking-wider text-emerald-100">Student Admission Portal</p>
   <h2 className="mt-2 text-2xl font-bold">Welcome, {user?.name?.split(' ')[0]||'Student'} 👋</h2>
   <p className="mt-2 max-w-2xl text-sm text-emerald-50/80">Complete your application, upload documents and track your admission progress from one place.</p>
   <button onClick={()=>nav('/student/application')} className="mt-5 inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-emerald-700">Open Application <ArrowRight size={16}/></button>
  </div>
  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
   {[[FileText,'Application',app?<Badge status={app.current_status}/>:<span className="text-slate-400">Not started</span>],[Upload,'Documents',`${verified}/${docs.length||0} verified`],[CheckCircle2,'Profile','Keep information updated'],[Clock,'Next action',app?.current_status==='draft'?'Submit application':'Check status']].map(([Icon,label,value])=><Card key={label}><div className="flex items-center gap-3"><div className="rounded-xl bg-emerald-50 p-3 text-emerald-600"><Icon size={19}/></div><div><p className="text-xs text-slate-400">{label}</p><div className="mt-1 text-sm font-semibold text-slate-800">{value}</div></div></div></Card>)}
  </div>
  <Card><h3 className="text-sm font-semibold">Admission workflow</h3><div className="mt-5 grid gap-3 md:grid-cols-5">{['Profile','Education','Preferences','Documents','Submit'].map((x,i)=><div key={x} className="rounded-xl border border-slate-100 p-4"><span className="text-xs font-bold text-emerald-600">0{i+1}</span><p className="mt-2 text-sm font-semibold">{x}</p><p className="mt-1 text-xs text-slate-400">{i===4?'Finalize application':'Complete this section'}</p></div>)}</div></Card>
 </div>
}
