import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, RefreshCw } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DataTable from '../../../components/crud/DataTable'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'
import { getFeeStructureList, deleteFeeStructure } from '../services'
import { feeStructureFields } from '../constants'

export default function FeeStructureListPage() {
  const navigate = useNavigate()
  const [rows, setRows] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [pendingDelete, setPendingDelete] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const load = () => {
    setIsLoading(true)
    setError('')
    getFeeStructureList()
      .then((data) => setRows(Array.isArray(data) ? data : data.items || []))
      .catch((err) => setError(err.message || 'Failed to load fee structure.'))
      .finally(() => setIsLoading(false))
  }

  useEffect(load, [])

  const columns = [
    { key: 'id', label: 'ID' },
    ...feeStructureFields
      .filter((f) => f.type !== 'textarea' && f.type !== 'password')
      .slice(0, 5)
      .map((f) => ({ key: f.name, label: f.label })),
  ]

  const handleDelete = () => {
    if (!pendingDelete) return
    setIsDeleting(true)
    deleteFeeStructure(pendingDelete.id)
      .then(() => {
        setPendingDelete(null)
        load()
      })
      .catch((err) => setError(err.message || 'Failed to delete record.'))
      .finally(() => setIsDeleting(false))
  }

  return (
    <div>
      <PageHeader
        title="Fee Structure"
        subtitle="Manage fee structure records."
        actions={
          <>
            <button
              onClick={load}
              className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              <RefreshCw size={16} />
              Refresh
            </button>
            <button
              onClick={() => navigate('/fee-structure/new')}
              className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700"
            >
              <Plus size={16} />
              Add New
            </button>
          </>
        }
      />

      <DataTable
        columns={columns}
        rows={rows}
        isLoading={isLoading}
        error={error}
        onView={(row) => navigate(`/fee-structure/${row.id}`)}
        onEdit={(row) => navigate(`/fee-structure/${row.id}/edit`)}
        onDelete={(row) => setPendingDelete(row)}
        emptyMessage="No fee structure found yet."
      />

      <ConfirmDialog
        open={!!pendingDelete}
        title="Delete record?"
        message="This action cannot be undone."
        isLoading={isDeleting}
        onConfirm={handleDelete}
        onCancel={() => setPendingDelete(null)}
      />
    </div>
  )
}
