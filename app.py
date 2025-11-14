from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import uuid, os, shutil

app = FastAPI()
os.makedirs('outputs', exist_ok=True)

@app.post('/api/run_sync')
async def run_sync(mixture_audio: UploadFile = File(...), target_sample: UploadFile = File(...)):
    job_id = str(uuid.uuid4())[:8]
    job_dir = os.path.join('outputs', job_id)
    os.makedirs(job_dir, exist_ok=True)
    mixture_path = os.path.join(job_dir, 'mixture_audio.wav')
    target_path = os.path.join(job_dir, 'target_sample.wav')
    with open(mixture_path, 'wb') as f:
        f.write(await mixture_audio.read())
    with open(target_path, 'wb') as f:
        f.write(await target_sample.read())
    # Mock processing: copy the target_sample as target_speaker.wav
    shutil.copyfile(target_path, os.path.join(job_dir, 'target_speaker.wav'))
    # Mock diarization JSON
    diar = [
        {"speaker":"Target","start":1.0,"end":4.2,"text":"Hello, this is a mock target.","confidence":0.98},
        {"speaker":"Speaker_B","start":4.3,"end":7.9,"text":"Mock other speaker response.","confidence":0.95}
    ]
    return JSONResponse({"job_id": job_id, "status":"done", "diarization": diar, "files": {"target_speaker": f"/outputs/{job_id}/target_speaker.wav"}})

@app.get('/outputs/{job_id}/target_speaker.wav')
async def get_target(job_id: str):
    path = os.path.join('outputs', job_id, 'target_speaker.wav')
    if os.path.exists(path):
        return FileResponse(path, media_type='audio/wav', filename='target_speaker.wav')
    return JSONResponse({"error":"not found"}, status_code=404)
