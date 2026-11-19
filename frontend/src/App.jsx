import { useCallback, useEffect, useMemo, useState } from 'react'
import brandLogo from './assets/Transformation Health Logo.png'
import './App.css'

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')
const TOKEN_KEY = 'thealth_access_token'
const EMPTY_CLIENT = {
  first_name: '',
  last_name: '',
  age: '',
  date_of_birth: '',
  phone_number: '',
  email: '',
  status: 'Active',
  parent_info: '',
  event: '',
  signup_date: new Date().toISOString().slice(0, 10),
}

function Icon({ name, size = 20 }) {
  const paths = {
    activity: <><path d="M3 12h4l3-8 4 16 3-8h4" /></>,
    arrow: <><path d="M5 12h14" /><path d="m13 6 6 6-6 6" /></>,
    calendar: <><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M16 3v4M8 3v4M3 11h18" /></>,
    check: <path d="m5 12 4 4L19 6" />,
    chevron: <path d="m9 18 6-6-6-6" />,
    close: <path d="m18 6-12 12M6 6l12 12" />,
    clients: <><path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="10" cy="7" r="4" /><path d="M20 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" /></>,
    email: <><rect x="3" y="5" width="18" height="14" rx="2" /><path d="m3 7 9 6 9-6" /></>,
    lock: <><rect x="4" y="11" width="16" height="10" rx="2" /><path d="M8 11V7a4 4 0 1 1 8 0v4" /></>,
    logout: <><path d="M10 17l5-5-5-5M15 12H3" /><path d="M12 3h7a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-7" /></>,
    phone: <><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.2 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.96.35 1.9.69 2.8a2 2 0 0 1-.45 2.11L8.08 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.84.57 2.8.69A2 2 0 0 1 22 16.92z" /></>,
    plus: <path d="M12 5v14M5 12h14" />,
    search: <><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></>,
    shield: <><path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z" /><path d="m9 12 2 2 4-4" /></>,
    user: <><circle cx="12" cy="8" r="4" /><path d="M5 21a7 7 0 0 1 14 0" /></>,
  }
  return (
    <svg aria-hidden="true" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {paths[name]}
    </svg>
  )
}

function displayError(error) {
  if (typeof error === 'string') return error
  if (Array.isArray(error)) return error.map((item) => item.msg).filter(Boolean).join(', ')
  return 'Something went wrong. Please try again.'
}

function formatDate(value) {
  if (!value) return 'Not provided'
  const date = new Date(`${value.slice(0, 10)}T00:00:00`)
  return Number.isNaN(date.getTime())
    ? value
    : new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric', year: 'numeric' }).format(date)
}

function statusStyle(status = '') {
  const normalized = status.toLowerCase()
  if (normalized.includes('active')) return 'status-active'
  if (normalized.includes('follow')) return 'status-followup'
  if (normalized.includes('inactive') || normalized.includes('closed')) return 'status-inactive'
  return 'status-neutral'
}

function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      await onLogin(email, password)
    } catch (loginError) {
      setError(displayError(loginError))
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="login-page">
      <section className="login-aside">
        <div className="brand brand-light"><img className="brand-logo" src={brandLogo} alt="Transformation Health" /></div>
        <div className="login-message">
          <div className="eyebrow">OUTREACH TEAM WORKSPACE</div>
          <h1>Care starts<br />with connection.</h1>
          <p>A thoughtful space for our team to stay connected with the people we serve.</p>
        </div>
        <div className="login-aside-footer"><Icon name="shield" size={17} /> Internal employee access</div>
      </section>
      <section className="login-content">
        <div className="login-card">
          <div className="mobile-brand brand"><img className="brand-logo" src={brandLogo} alt="Transformation Health" /></div>
          <div className="login-icon"><Icon name="user" size={23} /></div>
          <p className="eyebrow">WELCOME BACK</p>
          <h2>Sign in to your account</h2>
          <p className="login-intro">Use your work email and password to continue.</p>
          {error && <div className="alert alert-error" role="alert">{error}</div>}
          <form onSubmit={submit} className="login-form">
            <label htmlFor="email">Work email</label>
            <div className="input-wrap">
              <Icon name="email" size={18} />
              <input id="email" type="email" autoComplete="username" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@transformationhealth.org" required />
            </div>
            <label htmlFor="password">Password</label>
            <div className="input-wrap">
              <Icon name="lock" size={18} />
              <input id="password" type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Enter your password" required />
            </div>
            <button type="submit" className="button button-primary login-submit" disabled={loading}>
              {loading ? 'Signing in…' : 'Sign in'} {!loading && <Icon name="arrow" size={18} />}
            </button>
          </form>
          <p className="login-help">Need access? Contact your team administrator.</p>
        </div>
        <footer className="login-footer">Transformation Health · Employee portal</footer>
      </section>
    </main>
  )
}

function ClientForm({ client, onClose, onSave, saving, error }) {
  const [values, setValues] = useState(client || EMPTY_CLIENT)
  const editing = Boolean(client?.id)

  function updateField(event) {
    setValues((current) => ({ ...current, [event.target.name]: event.target.value }))
  }

  function submit(event) {
    event.preventDefault()
    onSave({
      ...values,
      age: Number(values.age),
    })
  }

  return (
    <div className="modal-backdrop" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="client-modal" role="dialog" aria-modal="true" aria-labelledby="client-form-title">
        <header className="modal-header">
          <div><p className="eyebrow">{editing ? 'CLIENT RECORD' : 'NEW RECORD'}</p><h2 id="client-form-title">{editing ? 'Edit client' : 'Add a client'}</h2></div>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Close"><Icon name="close" /></button>
        </header>
        {error && <div className="alert alert-error" role="alert">{error}</div>}
        <form className="client-form" onSubmit={submit}>
          <div className="form-grid">
            <label>First name<input name="first_name" value={values.first_name} onChange={updateField} required /></label>
            <label>Last name<input name="last_name" value={values.last_name} onChange={updateField} required /></label>
            <label>Date of birth<input name="date_of_birth" type="date" value={values.date_of_birth} onChange={updateField} required /></label>
            <label>Age<input name="age" type="number" min="0" max="125" value={values.age} onChange={updateField} required /></label>
            <label>Phone<input name="phone_number" type="tel" value={values.phone_number} onChange={updateField} required /></label>
            <label>Email<input name="email" type="email" value={values.email} onChange={updateField} required /></label>
            <label>Status<input name="status" value={values.status} onChange={updateField} placeholder="Active" required /></label>
            <label>Signup date<input name="signup_date" type="date" value={values.signup_date} onChange={updateField} required /></label>
            <label className="form-span">Parent / guardian information<input name="parent_info" value={values.parent_info} onChange={updateField} required /></label>
            <label className="form-span">Referral event / source<input name="event" value={values.event} onChange={updateField} required /></label>
          </div>
          <div className="modal-actions">
            <button className="button button-secondary" type="button" onClick={onClose}>Cancel</button>
            <button className="button button-primary" type="submit" disabled={saving}>{saving ? 'Saving…' : editing ? 'Save changes' : 'Add client'}</button>
          </div>
        </form>
      </section>
    </div>
  )
}

function ClientDetails({ client, onClose, onEdit }) {
  return (
    <div className="modal-backdrop detail-backdrop" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="details-panel" role="dialog" aria-modal="true" aria-labelledby="client-name">
        <header className="details-header">
          <button className="icon-button" type="button" onClick={onClose} aria-label="Close details"><Icon name="close" /></button>
          <button className="button button-secondary edit-button" type="button" onClick={onEdit}>Edit record</button>
        </header>
        <div className="details-profile">
          <div className="client-avatar large">{client.first_name?.[0]}{client.last_name?.[0]}</div>
          <span className={`status-pill ${statusStyle(client.status)}`}>{client.status}</span>
          <h2 id="client-name">{client.first_name} {client.last_name}</h2>
          <p>Client record</p>
        </div>
        <div className="detail-list">
          <Detail icon="user" label="Age & date of birth" value={`${client.age} years · ${formatDate(client.date_of_birth)}`} />
          <Detail icon="phone" label="Phone" value={client.phone_number} />
          <Detail icon="email" label="Email" value={client.email} />
          <Detail icon="calendar" label="Signup date" value={formatDate(client.signup_date)} />
          <Detail icon="clients" label="Parent / guardian information" value={client.parent_info} />
          <Detail icon="activity" label="Referral event / source" value={client.event} />
        </div>
        <p className="record-note"><Icon name="shield" size={16} /> Client information is for authorized team use only.</p>
      </section>
    </div>
  )
}

function Detail({ icon, label, value }) {
  return <div className="detail-item"><span className="detail-icon"><Icon name={icon} size={18} /></span><div><span className="detail-label">{label}</span><p>{value || 'Not provided'}</p></div></div>
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(Boolean(localStorage.getItem(TOKEN_KEY)))
  const [pageError, setPageError] = useState('')
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('All clients')
  const [selectedClient, setSelectedClient] = useState(null)
  const [formClient, setFormClient] = useState(null)
  const [formError, setFormError] = useState('')
  const [saving, setSaving] = useState(false)

  const signOut = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
    setClients([])
    setSelectedClient(null)
    setFormClient(null)
  }, [])

  const request = useCallback(async (path, options = {}) => {
    const headers = new Headers(options.headers || {})
    if (token) headers.set('Authorization', `Bearer ${token}`)
    if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
    let response
    try {
      response = await fetch(`${API_URL}${path}`, { ...options, headers })
    } catch {
      throw new Error(`Could not connect to the server at ${API_URL}. Check that the backend is running.`)
    }
    if (response.status === 401 && token) {
      const error = new Error('Your session has expired. Please sign in again.')
      error.status = response.status
      throw error
    }
    if (!response.ok) {
      const body = await response.json().catch(() => null)
      const error = new Error(displayError(body?.detail) || `Request failed (${response.status}).`)
      error.status = response.status
      throw error
    }
    return response.status === 204 ? null : response.json()
  }, [token])

  const loadClients = useCallback(async () => {
    try {
      const data = await request('/clients/')
      setClients(Array.isArray(data) ? data : [])
    } catch (error) {
      if (error.status === 401) signOut()
      setPageError(error.message)
    } finally {
      setLoading(false)
    }
  }, [request, signOut])

  useEffect(() => {
    if (!token) return
    request('/clients/')
      .then((data) => setClients(Array.isArray(data) ? data : []))
      .catch((error) => {
        if (error.status === 401) signOut()
        setPageError(error.message)
      })
      .finally(() => setLoading(false))
  }, [token, request, signOut])

  async function login(email, password) {
    const body = new URLSearchParams({ username: email, password })
    let response
    try {
      response = await fetch(`${API_URL}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
      })
    } catch {
      throw new Error(`Could not connect to the server at ${API_URL}. Check that the backend is running.`)
    }
    const result = await response.json().catch(() => null)
    if (!response.ok) throw new Error(displayError(result?.detail) || 'Unable to sign in. Please check your credentials.')
    if (!result?.access_token) throw new Error('The server did not return an access token.')
    localStorage.setItem(TOKEN_KEY, result.access_token)
    setPageError('')
    setLoading(true)
    setToken(result.access_token)
  }

  async function saveClient(values) {
    setSaving(true)
    setFormError('')
    const editing = Boolean(formClient?.id)
    try {
      const saved = await request(editing ? `/clients/${formClient.id}` : '/clients/', {
        method: editing ? 'PUT' : 'POST',
        body: JSON.stringify(values),
      })
      setClients((current) => editing
        ? current.map((client) => client.id === saved.id ? saved : client)
        : [saved, ...current])
      setSelectedClient(editing ? saved : null)
      setFormClient(null)
    } catch (error) {
      if (error.status === 401) signOut()
      else setFormError(error.message)
    } finally {
      setSaving(false)
    }
  }

  const activeCount = clients.filter((client) => client.status?.toLowerCase().includes('active') && !client.status?.toLowerCase().includes('inactive')).length
  const followupCount = clients.filter((client) => client.status?.toLowerCase().includes('follow')).length
  const filteredClients = useMemo(() => {
    const query = search.trim().toLowerCase()
    return [...clients]
      .filter((client) => statusFilter === 'All clients' || client.status?.toLowerCase() === statusFilter.toLowerCase())
      .filter((client) => !query || [
        client.first_name, client.last_name, client.email, client.phone_number, client.status, client.event,
      ].some((value) => String(value || '').toLowerCase().includes(query)))
      .sort((a, b) => String(b.signup_date || '').localeCompare(String(a.signup_date || '')))
  }, [clients, search, statusFilter])

  if (!token) return <Login onLogin={login} />

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><img className="brand-logo" src={brandLogo} alt="Transformation Health" /></div>
        <div className="workspace-label">WORKSPACE</div>
        <button className="nav-item active"><Icon name="clients" size={19} /> Clients <span className="nav-count">{clients.length}</span></button>
        <div className="sidebar-bottom">
          <div className="privacy-card"><span className="privacy-icon"><Icon name="shield" size={18} /></span><div><strong>Private workspace</strong><p>For authorized employees only</p></div></div>
          <button className="profile-button" onClick={signOut}>
            <span className="profile-avatar"><Icon name="user" size={17} /></span>
            <span className="profile-copy"><strong>Outreach team</strong><small>Employee account</small></span>
            <Icon name="logout" size={17} />
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumbs">Workspace <Icon name="chevron" size={15} /> <strong>Clients</strong></div>
          <div className="topbar-right"><span className="secure-label"><Icon name="shield" size={15} /> Employee portal</span><button className="mobile-logout" onClick={signOut} aria-label="Sign out"><Icon name="logout" /></button></div>
        </header>

        <div className="page-content">
          <div className="page-heading">
            <div><p className="eyebrow">CLIENT RELATIONSHIPS</p><h1>Clients</h1><p className="page-subtitle">A clear view of the people and relationships your team supports.</p></div>
            <button className="button button-primary add-button" onClick={() => { setFormError(''); setFormClient({ ...EMPTY_CLIENT }) }}><Icon name="plus" size={18} /> Add client</button>
          </div>

          <section className="stats-grid" aria-label="Client overview">
            <article className="stat-card"><div className="stat-icon blue"><Icon name="clients" /></div><div><span>Total clients</span><strong>{clients.length}</strong></div><small>In your workspace</small></article>
            <article className="stat-card"><div className="stat-icon green"><Icon name="check" /></div><div><span>Active</span><strong>{activeCount}</strong></div><small>Currently receiving support</small></article>
            <article className="stat-card"><div className="stat-icon amber"><Icon name="calendar" /></div><div><span>Follow-up</span><strong>{followupCount}</strong></div><small>Marked for follow-up</small></article>
          </section>

          <section className="clients-card">
            <div className="list-heading">
              <div><h2>Client directory</h2><p>Manage and review client records</p></div>
              <div className="list-controls">
                <label className="search-box"><Icon name="search" size={18} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search clients…" aria-label="Search clients" /></label>
                <select className="filter-select" value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} aria-label="Filter by status">
                  <option>All clients</option>
                  {[...new Set(clients.map((client) => client.status).filter(Boolean))].sort().map((status) => <option key={status}>{status}</option>)}
                </select>
              </div>
            </div>
            {pageError && <div className="alert alert-error page-alert" role="alert"><span>{pageError}</span><button className="text-button" onClick={() => { setPageError(''); setLoading(true); loadClients() }}>Try again</button></div>}
            <div className="client-table-wrap">
              <table className="client-table">
                <thead><tr><th>CLIENT</th><th>STATUS</th><th>PHONE</th><th>SIGNUP DATE</th><th>REFERRAL SOURCE</th><th><span className="sr-only">Open record</span></th></tr></thead>
                <tbody>
                  {loading ? <tr><td className="table-state" colSpan="6"><span className="spinner" /> Loading client records…</td></tr>
                    : filteredClients.length === 0 ? <tr><td className="table-state" colSpan="6"><div className="empty-icon"><Icon name="clients" size={22} /></div><strong>{clients.length === 0 ? 'No client records yet' : 'No matching clients'}</strong><p>{clients.length === 0 ? 'Add a client to get started with your directory.' : 'Try a different search or status filter.'}</p>{clients.length === 0 && <button className="button button-primary empty-add" onClick={() => { setFormError(''); setFormClient({ ...EMPTY_CLIENT }) }}><Icon name="plus" size={17} /> Add client</button>}</td></tr>
                    : filteredClients.map((client) => <tr key={client.id} className="client-row" onClick={() => setSelectedClient(client)} tabIndex="0" onKeyDown={(event) => event.key === 'Enter' && setSelectedClient(client)}>
                      <td><div className="client-cell"><span className="client-avatar">{client.first_name?.[0]}{client.last_name?.[0]}</span><span><strong>{client.first_name} {client.last_name}</strong><small>{client.email}</small></span></div></td>
                      <td><span className={`status-pill ${statusStyle(client.status)}`}><span />{client.status}</span></td>
                      <td className="muted-cell">{client.phone_number}</td>
                      <td className="muted-cell">{formatDate(client.signup_date)}</td>
                      <td className="muted-cell">{client.event || '—'}</td>
                      <td><button className="row-open" aria-label={`View ${client.first_name} ${client.last_name}`} onClick={(event) => { event.stopPropagation(); setSelectedClient(client) }}><Icon name="chevron" size={18} /></button></td>
                    </tr>)}
                </tbody>
              </table>
            </div>
            {!loading && filteredClients.length > 0 && <div className="list-footer">Showing <strong>{filteredClients.length}</strong> of <strong>{clients.length}</strong> client records</div>}
          </section>
          <footer className="main-footer"><span>Transformation Health · Outreach workspace</span><span><Icon name="shield" size={14} /> Handle client information with care</span></footer>
        </div>
      </main>
      {selectedClient && <ClientDetails client={selectedClient} onClose={() => setSelectedClient(null)} onEdit={() => { setFormError(''); setFormClient(selectedClient); setSelectedClient(null) }} />}
      {formClient && <ClientForm client={formClient} onClose={() => setFormClient(null)} onSave={saveClient} saving={saving} error={formError} />}
    </div>
  )
}

export default App
