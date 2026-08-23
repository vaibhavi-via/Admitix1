 import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Plus,
  RefreshCw,
  Search,
  SlidersHorizontal,
  Building2,
  X,
} from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DataTable from '../../../components/crud/DataTable'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'
import { getInstitutionsList, deleteInstitution } from '../services'
import { institutionsFields } from '../constants'
import { loadRelationOptions } from '../../../components/crud/relationOptions'

export default function InstitutionsListPage() {
  const navigate = useNavigate()

  const [rows, setRows] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [pendingDelete, setPendingDelete] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const [domainLabels, setDomainLabels] = useState({})

  const [search, setSearch] = useState('')
  const [showFilters, setShowFilters] = useState(false)

  const load = () => {
    setIsLoading(true)
    setError('')

    getInstitutionsList()
      .then((data) =>
        setRows(Array.isArray(data) ? data : data.items || []),
      )
      .catch((err) =>
        setError(err.message || 'Failed to load institutions.'),
      )
      .finally(() => setIsLoading(false))
  }

  useEffect(load, [])

  // Resolve domain_id -> "Engineering (ENG)" once, so the table shows
  // a readable domain name/badge instead of a raw foreign-key UUID.
  useEffect(() => {
    loadRelationOptions('domain')
      .then((options) => {
        const map = {}
        options.forEach((opt) => {
          map[opt.value] = opt.label
        })
        setDomainLabels(map)
      })
      .catch(() => {
        // Non-fatal: the domain column just falls back to the raw
        // (truncated) id if the lookup fails.
      })
  }, [])

  const columns = [
    ...institutionsFields
      .filter((f) => f.type !== 'textarea' && f.type !== 'password')
      .slice(0, 5)
      .map((f) => {
        if (f.name === 'domain_id') {
          return {
            key: f.name,
            label: 'Domain',
            render: (row) => {
              const label = domainLabels[row.domain_id]
              if (!label) {
                return <span className="text-slate-400">—</span>
              }
              return (
                <span className="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-semibold text-emerald-700">
                  {label}
                </span>
              )
            },
          }
        }
        return { key: f.name, label: f.label }
      }),
  ]

  const filteredRows = rows.filter((row) => {
    if (!search.trim()) return true

    const query = search.toLowerCase()

    return Object.values(row).some((value) =>
      String(value ?? '')
        .toLowerCase()
        .includes(query),
    )
  })

  const handleDelete = () => {
    if (!pendingDelete) return

    setIsDeleting(true)

    deleteInstitution(pendingDelete.id)
      .then(() => {
        setPendingDelete(null)
        load()
      })
      .catch((err) =>
        setError(err.message || 'Failed to delete record.'),
      )
      .finally(() => setIsDeleting(false))
  }

  const clearSearch = () => {
    setSearch('')
  }

  return (
    <div className="mx-auto max-w-[1600px]">
      {/* Page header */}
      <PageHeader
        title="Institutions"
        subtitle="Manage institutions and their registration information."
        actions={
          <>
            <button
              onClick={load}
              disabled={isLoading}
              className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 shadow-sm transition hover:bg-slate-50 hover:text-slate-900 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RefreshCw
                size={16}
                className={isLoading ? 'animate-spin' : ''}
              />
              Refresh
            </button>

            <button
              onClick={() => navigate('/institutions/new')}
              className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-emerald-600/20 transition hover:bg-emerald-700"
            >
              <Plus size={17} />
              Add Institution
            </button>
          </>
        }
      />

      {/* Main card */}
      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        {/* Toolbar */}
        <div className="border-b border-slate-100 p-4 sm:p-5">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            {/* Search */}
            <div className="relative w-full lg:max-w-md">
              <Search
                size={18}
                className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400"
              />

              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search institutions..."
                className="!w-full !rounded-xl !border-slate-200 !bg-slate-50 !py-2.5 !pl-10 !pr-10 !text-sm focus:!border-emerald-500 focus:!bg-white focus:!ring-4 focus:!ring-emerald-50"
              />

              {search && (
                <button
                  onClick={clearSearch}
                  className="absolute right-3 top-1/2 flex -translate-y-1/2 items-center justify-center rounded-md p-1 text-slate-400 hover:bg-slate-200 hover:text-slate-700"
                >
                  <X size={15} />
                </button>
              )}
            </div>

            {/* Toolbar actions */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowFilters((value) => !value)}
                className={`inline-flex items-center gap-2 rounded-xl border px-3.5 py-2.5 text-sm font-medium transition ${
                  showFilters
                    ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                    : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'
                }`}
              >
                <SlidersHorizontal size={16} />
                Filters
              </button>

              <div className="hidden h-8 w-px bg-slate-200 sm:block" />

              <div className="flex items-center gap-2 rounded-xl bg-slate-50 px-3.5 py-2.5">
                <Building2 size={15} className="text-slate-400" />

                <span className="text-xs font-medium text-slate-500">
                  {search
                    ? `${filteredRows.length} of ${rows.length}`
                    : `${rows.length}`}{' '}
                  {rows.length === 1 ? 'institution' : 'institutions'}
                </span>
              </div>
            </div>
          </div>

          {/* Filter panel placeholder */}
          {showFilters && (
            <div className="mt-4 rounded-xl border border-emerald-100 bg-emerald-50/50 p-4">
              <div className="flex items-start gap-3">
                <SlidersHorizontal
                  size={17}
                  className="mt-0.5 text-emerald-600"
                />

                <div>
                  <p className="text-sm font-semibold text-slate-800">
                    Filters
                  </p>

                  <p className="mt-0.5 text-xs text-slate-500">
                    Additional institution filters can be added here when
                    needed.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Search result information */}
        {search && !isLoading && !error && (
          <div className="flex items-center justify-between border-b border-slate-100 bg-slate-50/50 px-4 py-2.5 sm:px-5">
            <p className="text-xs text-slate-500">
              Showing results for{' '}
              <span className="font-semibold text-slate-700">
                "{search}"
              </span>
            </p>

            <button
              onClick={clearSearch}
              className="text-xs font-semibold text-emerald-600 hover:text-emerald-700"
            >
              Clear search
            </button>
          </div>
        )}

        {/* Table */}
        <DataTable
          columns={columns}
          rows={filteredRows}
          isLoading={isLoading}
          error={error}
          onView={(row) => navigate(`/institutions/${row.id}`)}
          onEdit={(row) => navigate(`/institutions/${row.id}/edit`)}
          onDelete={(row) => setPendingDelete(row)}
          emptyMessage={
            search
              ? 'No institutions match your search.'
              : 'No institutions have been added yet.'
          }
        />
      </div>

      {/* Delete dialog */}
      <ConfirmDialog
        open={!!pendingDelete}
        title="Delete institution?"
        message={
          pendingDelete
            ? `You are about to delete "${pendingDelete.institution_name || pendingDelete.name || 'this institution'}". This action cannot be undone.`
            : 'This action cannot be undone.'
        }
        confirmLabel="Delete Institution"
        isLoading={isDeleting}
        onConfirm={handleDelete}
        onCancel={() => setPendingDelete(null)}
      />
    </div>
  )
}