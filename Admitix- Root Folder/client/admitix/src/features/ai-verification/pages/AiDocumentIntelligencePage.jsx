import { useMemo, useState } from 'react'
import {
  AlertTriangle,
  CheckCircle2,
  FileCheck2,
  FileText,
  GitCompare,
  Loader2,
  ScanSearch,
  Sparkles,
  Upload,
  XCircle,
} from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import {
  crossVerifyDocuments,
  extractDocumentOCR,
  verifyDocumentWithAI,
} from '../aiServices'

const TABS = [
  { id: 'ocr', label: 'OCR & Data Extraction', icon: ScanSearch },
  { id: 'verify', label: 'AI Document Verification', icon: FileCheck2 },
  { id: 'cross', label: 'Cross-Document Verification', icon: GitCompare },
]

const ACCEPT = '.pdf,.jpg,.jpeg,.png,.webp'

function statusTone(status) {
  if (['passed', 'consistent', 'match'].includes(status)) return 'text-emerald-700 bg-emerald-50 border-emerald-200'
  if (['failed', 'mismatch'].includes(status)) return 'text-red-700 bg-red-50 border-red-200'
  return 'text-amber-700 bg-amber-50 border-amber-200'
}

function Score({ label, value }) {
  if (value == null) return null
  return (
    <div className="rounded-xl border border-gray-200 bg-gray-50 p-3">
      <div className="flex items-center justify-between gap-3">
        <span className="text-xs font-medium text-gray-500">{label}</span>
        <span className="text-sm font-bold text-gray-900">{Math.round(Number(value))}%</span>
      </div>
      <div className="mt-2 h-2 overflow-hidden rounded-full bg-gray-200">
        <div
          className="h-full rounded-full bg-emerald-500 transition-all"
          style={{ width: `${Math.max(0, Math.min(100, Number(value)))}%` }}
        />
      </div>
    </div>
  )
}

function FilePicker({ multiple, files, setFiles }) {
  const onChange = (event) => {
    const selected = Array.from(event.target.files || [])
    setFiles(multiple ? selected.slice(0, 5) : selected.slice(0, 1))
    event.target.value = ''
  }

  return (
    <div>
      <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-300 bg-gray-50 px-6 py-10 text-center transition hover:border-emerald-400 hover:bg-emerald-50/40">
        <span className="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-white text-emerald-600 shadow-sm">
          <Upload size={22} />
        </span>
        <span className="text-sm font-semibold text-gray-800">
          {multiple ? 'Choose 2–5 documents to compare' : 'Choose a document to analyze'}
        </span>
        <span className="mt-1 text-xs text-gray-500">PDF, JPG, PNG or WEBP · maximum 12 MB per file</span>
        <input type="file" accept={ACCEPT} multiple={multiple} onChange={onChange} className="hidden" />
      </label>

      {files.length > 0 && (
        <div className="mt-4 space-y-2">
          {files.map((file) => (
            <div key={`${file.name}-${file.size}`} className="flex items-center gap-3 rounded-xl border border-gray-200 bg-white px-3 py-2.5">
              <FileText size={17} className="shrink-0 text-emerald-600" />
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-gray-800">{file.name}</p>
                <p className="text-xs text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
              <button type="button" onClick={() => setFiles(files.filter((item) => item !== file))} className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-700">
                <XCircle size={17} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function ResultCard({ children }) {
  return <div className="mt-6 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">{children}</div>
}

function OcrResult({ result }) {
  return (
    <ResultCard>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-emerald-600">OCR Result</p>
          <h3 className="mt-1 text-lg font-semibold text-gray-900">{result.document_type || 'Document'}</h3>
          <p className="mt-1 text-xs text-gray-500">{result.file_name}</p>
        </div>
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2 text-center">
          <p className="text-[11px] font-medium text-emerald-600">Extraction confidence</p>
          <p className="text-xl font-bold text-emerald-700">{Math.round(Number(result.confidence_score || 0))}%</p>
        </div>
      </div>

      <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {Object.entries(result.fields || {}).map(([key, value]) => (
          <div key={key} className="rounded-xl border border-gray-100 bg-gray-50 p-3">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-gray-400">{key.replaceAll('_', ' ')}</p>
            <p className="mt-1 break-words text-sm font-medium text-gray-800">{value || '—'}</p>
          </div>
        ))}
      </div>

      {result.additional_fields && Object.keys(result.additional_fields).length > 0 && (
        <div className="mt-5">
          <p className="mb-2 text-sm font-semibold text-gray-800">Additional extracted fields</p>
          <pre className="max-h-64 overflow-auto rounded-xl bg-gray-950 p-4 text-xs leading-5 text-gray-100">{JSON.stringify(result.additional_fields, null, 2)}</pre>
        </div>
      )}

      <div className="mt-5">
        <p className="mb-2 text-sm font-semibold text-gray-800">OCR text</p>
        <pre className="max-h-80 overflow-auto whitespace-pre-wrap rounded-xl border border-gray-200 bg-gray-50 p-4 text-xs leading-5 text-gray-700">{result.raw_text || 'No readable text was returned.'}</pre>
      </div>
    </ResultCard>
  )
}

function VerificationResult({ result }) {
  const checks = result.checks || []
  return (
    <ResultCard>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-indigo-600">AI screening result</p>
          <h3 className="mt-1 text-lg font-semibold text-gray-900">{result.document_type || 'Document'}</h3>
          <p className="mt-1 text-xs text-gray-500">{result.file_name}</p>
        </div>
        <span className={`rounded-full border px-3 py-1.5 text-xs font-bold uppercase ${statusTone(result.decision)}`}>
          {result.decision || 'manual_review'}
        </span>
      </div>

      <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Score label="Overall confidence" value={result.confidence_score} />
        <Score label="Legibility" value={result.quality?.legibility} />
        <Score label="Blur risk score" value={result.quality?.blur_risk} />
        <Score label="Tampering risk score" value={result.quality?.tampering_risk} />
      </div>

      <div className="mt-5 space-y-2">
        {checks.map((check, index) => (
          <div key={`${check.name}-${index}`} className="flex items-start gap-3 rounded-xl border border-gray-100 bg-gray-50 p-3">
            {check.status === 'passed' ? <CheckCircle2 size={18} className="mt-0.5 shrink-0 text-emerald-600" /> : check.status === 'failed' ? <XCircle size={18} className="mt-0.5 shrink-0 text-red-600" /> : <AlertTriangle size={18} className="mt-0.5 shrink-0 text-amber-600" />}
            <div>
              <p className="text-sm font-semibold text-gray-800">{check.name}</p>
              <p className="mt-0.5 text-xs leading-5 text-gray-500">{check.details}</p>
            </div>
          </div>
        ))}
      </div>

      {result.issues?.length > 0 && (
        <div className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-4">
          <p className="text-sm font-semibold text-amber-800">Review flags</p>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-xs leading-5 text-amber-700">{result.issues.map((issue, index) => <li key={index}>{issue}</li>)}</ul>
        </div>
      )}

      <div className="mt-5 rounded-xl border border-gray-200 bg-gray-50 p-4">
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Recommended action</p>
        <p className="mt-1 text-sm text-gray-700">{result.recommended_action || 'Review the document manually before making a final decision.'}</p>
      </div>
    </ResultCard>
  )
}

function CrossResult({ result }) {
  return (
    <ResultCard>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-violet-600">Cross-document result</p>
          <h3 className="mt-1 text-lg font-semibold text-gray-900">Identity & field consistency</h3>
          <p className="mt-1 text-xs text-gray-500">Compared {result.file_names?.length || 0} uploaded documents</p>
        </div>
        <span className={`rounded-full border px-3 py-1.5 text-xs font-bold uppercase ${statusTone(result.overall_status)}`}>
          {String(result.overall_status || 'manual_review').replaceAll('_', ' ')}
        </span>
      </div>

      <div className="mt-5 flex items-center gap-3 rounded-xl border border-gray-200 bg-gray-50 p-4">
        <GitCompare size={20} className="text-violet-600" />
        <div>
          <p className="text-xs text-gray-500">Overall comparison confidence</p>
          <p className="text-lg font-bold text-gray-900">{Math.round(Number(result.overall_confidence || 0))}%</p>
        </div>
      </div>

      <div className="mt-5 overflow-x-auto rounded-xl border border-gray-200">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-gray-50 text-xs uppercase tracking-wide text-gray-500">
            <tr><th className="px-4 py-3">Field</th><th className="px-4 py-3">Status</th><th className="px-4 py-3">Observed values</th><th className="px-4 py-3">Details</th></tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {(result.comparisons || []).map((comparison, index) => (
              <tr key={`${comparison.field}-${index}`}>
                <td className="px-4 py-3 font-semibold text-gray-800">{comparison.field?.replaceAll('_', ' ')}</td>
                <td className="px-4 py-3"><span className={`rounded-full border px-2.5 py-1 text-[11px] font-bold uppercase ${statusTone(comparison.status)}`}>{comparison.status}</span></td>
                <td className="px-4 py-3 text-xs text-gray-600">{(comparison.values || []).map((item) => `${item.file_name}: ${item.value || '—'}`).join(' · ')}</td>
                <td className="px-4 py-3 text-xs leading-5 text-gray-500">{comparison.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {result.critical_mismatches?.length > 0 && (
        <div className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4">
          <p className="text-sm font-semibold text-red-800">Critical mismatches</p>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-xs leading-5 text-red-700">{result.critical_mismatches.map((item, index) => <li key={index}>{item}</li>)}</ul>
        </div>
      )}

      <div className="mt-5 rounded-xl border border-violet-200 bg-violet-50 p-4">
        <p className="text-xs font-semibold uppercase tracking-wider text-violet-500">Recommendation</p>
        <p className="mt-1 text-sm text-violet-900">{result.recommendation || 'Send the application to manual review when material mismatches are present.'}</p>
      </div>
    </ResultCard>
  )
}

export default function AiDocumentIntelligencePage() {
  const [activeTab, setActiveTab] = useState('ocr')
  const [files, setFiles] = useState([])
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [isRunning, setIsRunning] = useState(false)

  const multiple = activeTab === 'cross'
  const buttonLabel = useMemo(() => {
    if (activeTab === 'ocr') return 'Extract document data'
    if (activeTab === 'verify') return 'Run AI verification'
    return 'Compare documents'
  }, [activeTab])

  const switchTab = (tab) => {
    setActiveTab(tab)
    setFiles([])
    setResult(null)
    setError('')
  }

  const run = async () => {
    if (files.length === 0 || (multiple && files.length < 2)) {
      setError(multiple ? 'Select at least two documents to compare.' : 'Select a document first.')
      return
    }

    setIsRunning(true)
    setError('')
    setResult(null)
    try {
      if (activeTab === 'ocr') setResult(await extractDocumentOCR(files[0]))
      else if (activeTab === 'verify') setResult(await verifyDocumentWithAI(files[0]))
      else setResult(await crossVerifyDocuments(files))
    } catch (err) {
      setError(err.message || 'AI analysis failed. Please try again.')
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div>
      <PageHeader
        title="AI Document Intelligence"
        subtitle="OCR, document screening and cross-document consistency checks powered by Groq."
        actions={<div className="inline-flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs font-semibold text-emerald-700"><Sparkles size={15} /> AI workspace</div>}
      />

      <div className="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
        <div className="grid gap-2 md:grid-cols-3">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button key={id} type="button" onClick={() => switchTab(id)} className={`flex items-center gap-3 rounded-xl border px-4 py-3 text-left transition ${activeTab === id ? 'border-emerald-300 bg-emerald-50 text-emerald-800' : 'border-gray-200 bg-white text-gray-600 hover:bg-gray-50'}`}>
              <span className={`flex h-9 w-9 items-center justify-center rounded-lg ${activeTab === id ? 'bg-emerald-500 text-white' : 'bg-gray-100 text-gray-500'}`}><Icon size={18} /></span>
              <span className="text-sm font-semibold">{label}</span>
            </button>
          ))}
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-[1.1fr_.9fr]">
          <div>
            <FilePicker multiple={multiple} files={files} setFiles={setFiles} />
            {error && <div className="mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
            <button type="button" disabled={isRunning || files.length === 0} onClick={run} className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-50">
              {isRunning ? <><Loader2 size={17} className="animate-spin" /> Analyzing with AI…</> : <><Sparkles size={17} /> {buttonLabel}</>}
            </button>
          </div>

          <div className="rounded-2xl border border-gray-100 bg-gray-50 p-5">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">How this works</p>
            {activeTab === 'ocr' && <div className="mt-4 space-y-4"><Step n="1" title="Upload" text="Upload a student document as PDF or image." /><Step n="2" title="Read" text="The vision model reads the document and extracts visible fields." /><Step n="3" title="Review" text="See structured fields, confidence and the full OCR text." /></div>}
            {activeTab === 'verify' && <div className="mt-4 space-y-4"><Step n="1" title="Inspect" text="AI checks legibility, cropping and visible consistency signals." /><Step n="2" title="Score" text="A conservative confidence and risk assessment is generated." /><Step n="3" title="Route" text="Potential issues are flagged for manual review instead of blindly passing." /></div>}
            {activeTab === 'cross' && <div className="mt-4 space-y-4"><Step n="1" title="Upload 2–5 docs" text="Add identity, marksheet, certificate or other admission documents." /><Step n="2" title="Extract" text="The model reads the same identity and academic fields from each document." /><Step n="3" title="Compare" text="Names, DOB, parent name, institution and other fields are compared." /></div>}
          </div>
        </div>
      </div>

      {result && activeTab === 'ocr' && <OcrResult result={result} />}
      {result && activeTab === 'verify' && <VerificationResult result={result} />}
      {result && activeTab === 'cross' && <CrossResult result={result} />}

      <div className="mt-5 flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-xs leading-5 text-amber-800">
        <AlertTriangle size={17} className="mt-0.5 shrink-0" />
        <p><strong>Human review remains the final decision.</strong> AI screening can identify OCR, quality and consistency issues, but it should not be treated as legal or forensic proof of authenticity.</p>
      </div>
    </div>
  )
}

function Step({ n, title, text }) {
  return <div className="flex gap-3"><span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-white text-xs font-bold text-emerald-600 shadow-sm">{n}</span><div><p className="text-sm font-semibold text-gray-800">{title}</p><p className="mt-0.5 text-xs leading-5 text-gray-500">{text}</p></div></div>
}
