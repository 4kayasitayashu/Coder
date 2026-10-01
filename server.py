"""
FastAPI console for the Coder agent.

Run from your project root (same folder as main.py):
    pip install fastapi uvicorn websockets
    uvicorn server:app --reload

Then open http://127.0.0.1:8000
"""
import json
import pathlib

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from agent.graph import agent
from agent.tools import PROJECT_ROOT

IGNORE_DIRS = {".venv", "venv", "__pycache__", "node_modules", ".git", ".idea"}

app = FastAPI(title="Coder Agent Console")

PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

# Serve the frontend's own assets (if you add any) from /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the generated project so the "Preview" tab can render it directly
app.mount("/preview", StaticFiles(directory=str(PROJECT_ROOT), html=True), name="preview")


def _list_generated_files():
    return sorted(
        str(f.relative_to(PROJECT_ROOT))
        for f in PROJECT_ROOT.glob("**/*")
        if f.is_file() and not any(part in IGNORE_DIRS for part in f.parts)
    )


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/api/files")
async def api_list_files():
    return JSONResponse({"files": _list_generated_files()})


@app.get("/api/file")
async def api_get_file(path: str):
    p = (PROJECT_ROOT / path).resolve()
    if PROJECT_ROOT.resolve() not in p.parents and p != PROJECT_ROOT.resolve():
        return JSONResponse({"error": "invalid path"}, status_code=400)
    if not p.exists() or not p.is_file():
        return JSONResponse({"error": "not found"}, status_code=404)
    return JSONResponse({
        "path": path,
        "content": p.read_text(encoding="utf-8", errors="replace"),
    })


async def _send(ws: WebSocket, payload: dict):
    await ws.send_text(json.dumps(payload, default=str))


@app.websocket("/ws/generate")
async def ws_generate(ws: WebSocket):
    await ws.accept()
    try:
        raw = await ws.receive_text()
        data = json.loads(raw)
        user_prompt = (data.get("prompt") or "").strip()

        if not user_prompt:
            await _send(ws, {"type": "error", "message": "Prompt cannot be empty."})
            await ws.close()
            return

        await _send(ws, {"type": "stage", "stage": "planner", "status": "active"})

        steps_meta = None  # [{filepath, task_description}, ...] once architect finishes

        async for update in agent.astream(
            {"user_prompt": user_prompt},
            {"recursion_limit": 100},
            stream_mode="updates",
        ):
            for node, out in update.items():

                if node == "planner":
                    plan = out["plan"]
                    await _send(ws, {
                        "type": "stage", "stage": "planner", "status": "done",
                        "plan": plan.model_dump(),
                    })
                    await _send(ws, {"type": "stage", "stage": "architect", "status": "active"})

                elif node == "architect":
                    task_plan = out["task_plan"]
                    steps_meta = [
                        {"filepath": s.filepath, "task_description": s.task_description}
                        for s in task_plan.implementation_steps
                    ]
                    await _send(ws, {
                        "type": "stage", "stage": "architect", "status": "done",
                        "steps": steps_meta,
                    })
                    await _send(ws, {"type": "stage", "stage": "coder", "status": "active"})
                    if steps_meta:
                        await _send(ws, {
                            "type": "file_start",
                            "filepath": steps_meta[0]["filepath"],
                            "index": 0, "total": len(steps_meta),
                        })

                elif node == "coder":
                    coder_state = out.get("coder_state")
                    status = out.get("status")

                    if coder_state is not None and steps_meta:
                        idx = coder_state.current_step_idx
                        if 0 < idx <= len(steps_meta):
                            done_meta = steps_meta[idx - 1]
                            await _send(ws, {
                                "type": "file_done",
                                "filepath": done_meta["filepath"],
                                "index": idx, "total": len(steps_meta),
                            })
                        if idx < len(steps_meta):
                            await _send(ws, {
                                "type": "file_start",
                                "filepath": steps_meta[idx]["filepath"],
                                "index": idx, "total": len(steps_meta),
                            })

                    if status == "DONE":
                        await _send(ws, {"type": "stage", "stage": "coder", "status": "done"})

        files = _list_generated_files()
        preview_available = (PROJECT_ROOT / "index.html").exists()
        await _send(ws, {
            "type": "done",
            "files": files,
            "preview_available": preview_available,
        })

    except WebSocketDisconnect:
        pass
    except Exception as e:  # noqa: BLE001
        try:
            await _send(ws, {"type": "error", "message": str(e)})
        except Exception:
            pass
    finally:
        try:
            await ws.close()
        except Exception:
            pass
