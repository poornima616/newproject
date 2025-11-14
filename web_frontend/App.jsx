import React, {useState} from 'react';

export default function App(){
  const [mixture, setMixture] = useState(null);
  const [target, setTarget] = useState(null);
  const [result, setResult] = useState(null);

  async function upload(){
    if(!mixture || !target) return alert('Select files first');
    const fdata = new FormData();
    fdata.append('mixture_audio', mixture);
    fdata.append('target_sample', target);
    const res = await fetch('http://localhost:8000/api/run_sync', {method:'POST', body:fdata});
    const j = await res.json();
    setResult(j);
  }

  return (<div style={{padding:20,fontFamily:'Arial'}}>
    <h2>Unified Neural Pipeline — Prototype UI</h2>
    <p>Choose two files and click Run (this UI talks to the mock `app.py` server).</p>
    <div>
      <label>Mixture: <input type="file" onChange={e=>setMixture(e.target.files[0])} /></label>
    </div>
    <div>
      <label>Target sample: <input type="file" onChange={e=>setTarget(e.target.files[0])} /></label>
    </div>
    <button onClick={upload} style={{marginTop:10}}>Run</button>
    {result && <pre style={{marginTop:20,whiteSpace:'pre-wrap'}}>{JSON.stringify(result,null,2)}</pre>}
  </div>)
}
