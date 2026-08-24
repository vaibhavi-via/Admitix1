import {useEffect,useState} from 'react'
import {useNavigate} from 'react-router-dom'
import {Search,Clock,CheckCircle2,XCircle,ArrowRight,Wallet,RefreshCw} from 'lucide-react'
import {getApplications,getPaymentSummary} from './api'
import {Card,Badge,Loading,ErrorBox} from '../components/PortalUI'

export default function OfficerDashboardPage(){
 const [apps,setApps]=useState([]); const [payments,setPayments]=useState({}); const [loading,setLoading]=useState(true); const [error,setError]=useState(''); const nav=useNavigate()
 const load=async()=>{setLoading(true);setError('');try{const [a,p]=await Promise.all([getApplications(),getPaymentSummary()]);setApps(a||[]);setPayments(p||{})}catch(e){setError(e.message||'Unable to load officer dashboard.')}finally{setLoading(false)}}
 useEffect(()=>{load()},[])
 if(loading)return <Loading/>
 const count=s=>apps.filter(a=>a.current_status===s).length
 const success=payments.success?.total_amount??0
 return <div className="space-y-6">
  <div className="rounded-2xl bg-gradient-to-br from-emerald-700 via-emerald-600 to-green-500 p-6 text-white"><div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><div><p className="text-xs font-semibold uppercase tracking-wider text-emerald-100">Admission Officer Workspace</p><h2 className="mt-2 text-2xl font-bold">Application Review Center</h2><p className="mt-2 max-w-2xl text-sm text-emerald-50/80">Review assigned applications, verify documents, track payments and update admission decisions.</p></div><button onClick={load} className="inline-flex items-center gap-2 self-start rounded-lg bg-white/10 px-3 py-2 text-sm font-semibold hover:bg-white/20"><RefreshCw size={15}/> Refresh</button></div></div>
  <ErrorBox message={error}/>
  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
   {[[Search,'Assigned',apps.length],[Clock,'Under Review',count('under_review')],[CheckCircle2,'Approved',count('approved')],[XCircle,'Rejected',count('rejected')],[Wallet,'Collected',`₹${Number(success).toLocaleString()}`]].map(([I,l,v])=><Card key={l}><div className="flex items-center gap-3"><div className="rounded-xl bg-emerald-50 p-3 text-emerald-600"><I size={19}/></div><div><p className="text-xs text-slate-400">{l}</p><p className="mt-1 text-2xl font-bold">{v}</p></div></div></Card>)}
  </div>
  <Card><div className="flex items-center justify-between"><div><h3 className="font-semibold">Recent assigned applications</h3><p className="mt-1 text-xs text-slate-400">Only applications assigned to your staff account are shown.</p></div><button onClick={()=>nav('/officer/applications')} className="text-sm font-semibold text-emerald-600">View all</button></div>
   <div className="mt-4 divide-y divide-slate-100">{apps.slice(0,6).map(a=><button key={a.application_id} onClick={()=>nav(`/officer/applications/${a.application_id}`)} className="flex w-full items-center justify-between gap-3 py-3 text-left hover:bg-slate-50"><div><p className="text-sm font-semibold">{a.application_number}</p><p className="text-xs text-slate-400">Student ID: {String(a.student_id).slice(0,8)}...</p></div><div className="flex items-center gap-3"><Badge status={a.current_status}/><ArrowRight size={15} className="text-slate-300"/></div></button>)}</div>
   {!apps.length&&<p className="py-8 text-center text-sm text-slate-400">No applications are assigned to you yet.</p>}
  </Card>
 </div>
}
