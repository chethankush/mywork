from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import subprocess

app = FastAPI()

SERVICE = "httpd"

# -----------------------------
# Utility functions
# -----------------------------
def run_cmd(cmd):
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def get_status():
    out, err, rc = run_cmd(["systemctl", "is-active", SERVICE])
    return out  # active | inactive | failed


# -----------------------------
# API Endpoints
# -----------------------------
@app.get("/status")
def status():
    return JSONResponse({"service": SERVICE, "status": get_status()})


@app.post("/start")
def start():
    run_cmd(["systemctl", "start", SERVICE])
    return {"result": "started", "status": get_status()}


@app.post("/stop")
def stop():
    run_cmd(["systemctl", "stop", SERVICE])
    return {"result": "stopped", "status": get_status()}


@app.post("/restart")
def restart():
    run_cmd(["systemctl", "restart", SERVICE])
    return {"result": "restarted", "status": get_status()}


# -----------------------------
# Web UI
# -----------------------------
@app.get("/")
def index():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
<title>HTTPD Control Panel</title>
<style>
body { font-family: Arial; padding: 30px; }
button { padding: 10px 20px; margin: 5px; font-size: 16px; }
#status { margin-top: 20px; font-weight: bold; }
</style>
</head>
<body>

<h2>HTTPD Service Control</h2>

<button onclick="callApi('/start')">Start</button>
<button onclick="callApi('/stop')">Stop</button>
<button onclick="callApi('/restart')">Restart</button>

<div id="status">Checking status...</div>

<script>
async function callApi(endpoint) {
    await fetch(endpoint, { method: "POST" });
    updateStatus();
}

async function updateStatus() {
    const res = await fetch("/status");
    const data = await res.json();
    document.getElementById("status").innerText =
        "Status: " + data.status;
}

updateStatus();
setInterval(updateStatus, 3000);
</script>

</body>
</html>
""")

