import React, { useEffect, useState } from 'react'
import { Atom, FlaskConical, GitBranch, Activity, Beaker, History, ArrowUpRight, Sparkles, Terminal, CircleHelp } from 'lucide-react'
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const initial = { formula:'—', molecular_weight:'—', exact_mass:'—', logp:'—', tpsa:'—', functional_groups:[] }

function App() {
  const [tab, setTab] = useState('compound')
  const [smiles, setSmiles] = useState('CC(=O)OCC')
  const [compound, setCompound] = useState(initial)
  const [reaction, setReaction] = useState('hydrogenation')
  const [reactants, setReactants] = useState('C=C')
  const [reactionResult, setReactionResult] = useState(null)
  const [equation, setEquation] = useState('Fe + O2 -> Fe2O3')
  const [balance, setBalance] = useState(null)
  const [meanYield, setMeanYield] = useState('0.78')
  const [stdYield, setStdYield] = useState('0.06')
  const [simulation, setSimulation] = useState(null)
  const [history, setHistory] = useState([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  async function request(path, body) {
    setBusy(true); setError(''); setNotice('')
    try {
      const res = await fetch(`${API}${path}`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body) })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Request failed')
      setNotice('Analysis completed successfully')
      loadHistory()
      return data
    } catch (e) { setError(e.message); return null }
    finally { setBusy(false) }
  }
  async function loadHistory() {
    try { const r = await fetch(`${API}/api/history?limit=8`); if (r.ok) setHistory(await r.json()) } catch {}
  }
  useEffect(() => { loadHistory() }, [])

  async function analyze() { const d = await request('/api/compounds/analyze', {smiles}); if (d) setCompound(d) }
  async function predict() { const d = await request('/api/reactions/predict', {reaction, reactants:reactants.split(',').map(x=>x.trim()).filter(Boolean)}); if (d) setReactionResult(d) }
  async function balanceEq() { const d = await request('/api/stoichiometry/balance', {equation}); if (d) setBalance(d) }
  async function simulate() { const d = await request('/api/simulations/monte-carlo', {mean_yield:Number(meanYield), std_yield:Number(stdYield), trials:5000, seed:42}); if (d) setSimulation(d) }

  const nav = [
    ['compound','Compound intelligence',Atom], ['reaction','Reaction lab',GitBranch],
    ['stoich','Stoichiometry',Beaker], ['simulation','Monte Carlo lab',Activity]
  ]
  const chartData = simulation?.histogram?.map(x=>({range:`${Math.round(x.range_start*100)}–${Math.round(x.range_end*100)}%`, count:x.count})) || []

  return <div className="shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-icon"><Atom size={23}/></div><div><b>ChemFlow</b><span>AI LAB PLATFORM</span></div></div>
      <div className="workspace"><span className="workspace-dot"/> Research workspace <span className="chevron">⌄</span></div>
      <div className="nav-label">WORKSPACE</div>
      {nav.map(([id,label,Icon])=><button key={id} className={`nav-item ${tab===id?'active':''}`} onClick={()=>{setTab(id);setError('');setNotice('')}}><Icon size={17}/>{label}{tab===id&&<span className="nav-active"/>}</button>)}
      <div className="nav-label lower">SYSTEM</div>
      <button className="nav-item" onClick={loadHistory}><History size={17}/>Analysis history</button>
      <div className="sidebar-bottom"><div className="status"><span/> API connection <b>Local</b></div><div className="profile"><div className="avatar">CF</div><div><b>ChemFlow Lab</b><span>Educational edition</span></div><CircleHelp size={17}/></div></div>
    </aside>
    <main className="main">
      <header className="topbar"><div className="crumb">Workspace <span>/</span> <b>{nav.find(n=>n[0]===tab)?.[1]}</b></div><div className="top-right"><span className="live"><i/> SYSTEM OPERATIONAL</span><div className="top-avatar">CF</div></div></header>
      <div className="content">
        <div className="page-head"><div><div className="eyebrow"><Sparkles size={13}/> CHEMISTRY INTELLIGENCE</div><h1>{nav.find(n=>n[0]===tab)?.[1]}</h1><p>Explore molecular properties, reaction pathways, and quantitative chemistry.</p></div><div className="version">CHEMFLOW <b>2.0.0</b></div></div>
        <div className="stats">
          <div className="stat-card"><div className="stat-top"><span>ENGINE STATUS</span><Atom size={17}/></div><strong className="green">Ready</strong><small>RDKit molecular toolkit</small></div>
          <div className="stat-card"><div className="stat-top"><span>ACTIVE MODULES</span><FlaskConical size={17}/></div><strong>04</strong><small>Core chemistry services</small></div>
          <div className="stat-card"><div className="stat-top"><span>RECENT ANALYSES</span><History size={17}/></div><strong>{history.length.toString().padStart(2,'0')}</strong><small>Saved in local SQLite</small></div>
        </div>
        {error&&<div className="alert error">{error}</div>}{notice&&!error&&<div className="alert success">{notice}</div>}
        {tab==='compound'&&<section className="panel-grid">
          <div className="panel input-panel"><div className="panel-title"><div><span className="step">01</span><h2>Molecular input</h2></div><span className="tag">RDKit ENGINE</span></div><p className="muted">Enter a SMILES string to decode its molecular identity and physicochemical profile.</p>
            <label>SMILES NOTATION</label><textarea value={smiles} onChange={e=>setSmiles(e.target.value)} rows="3"/><div className="input-hint">Example: CCO (ethanol) · CC(=O)OCC (ethyl acetate)</div>
            <button className="primary" onClick={analyze} disabled={busy}>{busy?'Analyzing…':'Analyze compound'} <ArrowUpRight size={16}/></button>
            <div className="callout"><Sparkles size={16}/><span><b>What gets analyzed?</b> Molecular formula, exact mass, logP, TPSA, hydrogen bonding, rotatable bonds, and functional groups.</span></div>
          </div>
          <div className="panel result-panel"><div className="panel-title"><div><span className="step">02</span><h2>Compound profile</h2></div><span className="tag green-tag">LIVE RESULT</span></div>
            <div className="formula-box"><span>MOLECULAR FORMULA</span><strong>{compound.formula}</strong><small>Canonical SMILES: {compound.canonical_smiles||'Awaiting analysis'}</small></div>
            <div className="metrics"><Metric label="Molecular weight" value={compound.molecular_weight} unit="g/mol"/><Metric label="Exact mass" value={compound.exact_mass} unit="Da"/><Metric label="LogP" value={compound.logp} unit=""/><Metric label="TPSA" value={compound.tpsa} unit="Å²"/></div>
            <div className="group-section"><h3>Detected functional groups</h3><div className="chips">{compound.functional_groups.length?compound.functional_groups.map(g=><span className="chip" key={g}>{g.replaceAll('_',' ')}</span>):<span className="muted">Run an analysis to detect groups.</span>}</div></div>
            <div className="micro-grid"><div><span>H-BOND DONORS</span><b>{compound.h_bond_donors??'—'}</b></div><div><span>H-BOND ACCEPTORS</span><b>{compound.h_bond_acceptors??'—'}</b></div><div><span>ROTATABLE BONDS</span><b>{compound.rotatable_bonds??'—'}</b></div><div><span>HEAVY ATOMS</span><b>{compound.heavy_atoms??'—'}</b></div></div>
          </div>
        </section>}
        {tab==='reaction'&&<section className="panel wide-panel"><div className="panel-title"><div><span className="step">01</span><h2>Template-based reaction prediction</h2></div><span className="tag">REACTION ENGINE</span></div><p className="muted">Choose one of the supported educational transformations. This is a transparent rule/template engine, not a general-purpose AI predictor.</p><div className="form-row"><div className="field"><label>REACTION TEMPLATE</label><select value={reaction} onChange={e=>setReaction(e.target.value)}><option value="hydrogenation">Alkene hydrogenation</option><option value="alcohol_oxidation">Primary alcohol oxidation</option><option value="ester_hydrolysis">Ester hydrolysis</option></select></div><div className="field"><label>REACTANT SMILES</label><input value={reactants} onChange={e=>setReactants(e.target.value)}/><small>Separate multiple reactants with commas.</small></div></div><button className="primary" onClick={predict} disabled={busy}>Predict candidate products <ArrowUpRight size={16}/></button>
          {reactionResult&&<div className="result-block"><h3>Prediction output</h3><p>{reactionResult.description}</p><div className="product-list">{reactionResult.products.length?reactionResult.products.map((p,i)=><div className="product-row" key={p}><span>PRODUCT {i+1}</span><code>{p}</code></div>):<div className="muted">No product matched this template for the supplied reactants.</div>}</div><div className="warning"><CircleHelp size={16}/>{reactionResult.scope_warning}</div></div>}
        </section>}
        {tab==='stoich'&&<section className="panel wide-panel"><div className="panel-title"><div><span className="step">01</span><h2>Equation balancer</h2></div><span className="tag">SYMPY ENGINE</span></div><p className="muted">Find the smallest whole-number stoichiometric coefficients using linear algebra.</p><label>UNBALANCED EQUATION</label><input className="equation-input" value={equation} onChange={e=>setEquation(e.target.value)}/><div className="input-hint">Try: H2 + O2 -&gt; H2O · Fe + O2 -&gt; Fe2O3 · C3H8 + O2 -&gt; CO2 + H2O</div><button className="primary" onClick={balanceEq} disabled={busy}>Balance equation <ArrowUpRight size={16}/></button>{balance&&<div className="balanced"><span>BALANCED EQUATION</span><strong>{balance.balanced_equation}</strong><small>Elements conserved: {balance.elements.join(', ')}</small></div>}
          <div className="info-strip"><Beaker size={18}/><span><b>Yield calculator API also available</b> — calculate the limiting reagent and theoretical product mass using balanced coefficients and measured starting moles.</span></div>
        </section>}
        {tab==='simulation'&&<section className="panel wide-panel"><div className="panel-title"><div><span className="step">01</span><h2>Reaction yield uncertainty</h2></div><span className="tag">NUMPY MONTE CARLO</span></div><p className="muted">Model a distribution of possible yields instead of relying on one deterministic estimate.</p><div className="form-row"><div className="field"><label>EXPECTED MEAN YIELD (0–1)</label><input type="number" min="0" max="1" step=".01" value={meanYield} onChange={e=>setMeanYield(e.target.value)}/></div><div className="field"><label>STANDARD DEVIATION (0–0.5)</label><input type="number" min="0" max=".5" step=".01" value={stdYield} onChange={e=>setStdYield(e.target.value)}/></div></div><button className="primary" onClick={simulate} disabled={busy}>Run 5,000 simulations <Activity size={16}/></button>
          {simulation&&<div className="simulation-output"><div className="sim-kpis"><Metric label="Simulated mean" value={`${(simulation.mean*100).toFixed(1)}%`}/><Metric label="5th percentile" value={`${(simulation.p05*100).toFixed(1)}%`}/><Metric label="95th percentile" value={`${(simulation.p95*100).toFixed(1)}%`}/><Metric label="P(yield ≥ 80%)" value={`${(simulation.probability_above_80_percent*100).toFixed(1)}%`}/></div><h3>Outcome distribution</h3><div className="chart"><ResponsiveContainer width="100%" height={230}><AreaChart data={chartData}><CartesianGrid strokeDasharray="3 3" stroke="#26324a"/><XAxis dataKey="range" stroke="#8995aa" tick={{fontSize:10}}/><YAxis stroke="#8995aa" tick={{fontSize:10}}/><Tooltip contentStyle={{background:'#111b2e',border:'1px solid #33415d',borderRadius:8}}/><Area type="monotone" dataKey="count" stroke="#54d6b1" fill="#54d6b1" fillOpacity={.18}/></AreaChart></ResponsiveContainer></div><small className="muted">{simulation.assumption}</small></div>}
        </section>}
        <section className="bottom-grid"><div className="panel history-panel"><div className="panel-title"><div><History size={17}/><h2>Recent activity</h2></div><span className="tag">LOCAL HISTORY</span></div>{history.length?history.slice(0,5).map(item=><div className="history-row" key={item.id}><span className="history-icon"><Terminal size={15}/></span><div><b>{item.kind} analysis</b><small>{item.input}</small></div><time>{item.created_at?.split(' ')[0]}</time></div>):<p className="muted">Your saved analyses will appear here after the first API request.</p>}</div><div className="panel scope-panel"><div className="panel-title"><div><CircleHelp size={17}/><h2>Scientific scope</h2></div></div><p>Results are generated from cheminformatics descriptors, explicit reaction templates, symbolic balancing, and user-defined uncertainty assumptions.</p><div className="scope-note">Educational demonstrator · Verify chemistry independently · Not a synthesis or safety authority</div></div></section>
        <footer>CHEMFLOW AI 2.0 <span>Built for explainable chemistry workflows</span><span>FASTAPI + REACT + RDKIT</span></footer>
      </div>
    </main>
  </div>
}
function Metric({label,value,unit=''}) { return <div className="metric"><span>{label}</span><b>{value??'—'} <small>{unit}</small></b></div> }
export default App
