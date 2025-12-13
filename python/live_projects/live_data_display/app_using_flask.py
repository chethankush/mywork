from flask import Flask, Response
import time

app = Flask(__name__)

def stream_file():
    with open("data.txt", "r") as f:
        f.seek(0, 2)  # tail -f behavior
        while True:
            line = f.readline()
            if line:
                yield f"data: {line.rstrip()}\n\n"
            else:
                time.sleep(1)

@app.route("/stream")
def stream():
    return Response(
        stream_file(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h2>Live Process Data</h2>
        <pre id="output"></pre>

        <script>
            const source = new EventSource("/stream");

            source.onmessage = function(event) {
                document.getElementById("output").textContent += event.data + "\\n";
            };

            source.onerror = function() {
                console.log("SSE error");
            };
        </script>
    </body>
    </html>
    """

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)

