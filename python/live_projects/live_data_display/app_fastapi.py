from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import time

app = FastAPI()

def stream_file():
    with open("data.txt", "r") as f:
        f.seek(0, 2)  # tail -f behavior
        while True:
            line = f.readline()
            if line:
                yield f"data: {line.rstrip()}\n\n"
            else:
                time.sleep(1)

@app.get("/stream")
def stream():
    return StreamingResponse(
        stream_file(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.get("/")
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <body>
        <h2>Live Process Data (FastAPI)</h2>
        <pre id="output"></pre>

        <script>
            const source = new EventSource("/stream");
            source.onmessage = function(event) {
                document.getElementById("output").textContent += event.data + "\\n";
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

