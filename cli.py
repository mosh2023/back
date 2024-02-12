from enum import Enum
import platform
import subprocess
import time
import typer as typer

app = typer.Typer()


class ProcessManager(str, Enum):
    uvicorn = "uvicorn"
    gunicorn = "gunicorn"


@app.command()
def dummy_command():
    pass


@app.command()
def game(
        manager: ProcessManager = ProcessManager.uvicorn,
        port: int = 5001,
        host: str = "localhost",
        workers: int = 1,
        reload: bool = False
):
    if platform.system() == "Windows" or manager == ProcessManager.uvicorn:
        run_args = [
            ProcessManager.uvicorn,
            "app.main:app",
            "--host",
            f"{host}",
            "--port",
            f"{port}",
            "--workers",
            f"{workers}",
        ]
        if reload:
            run_args.append("--reload")
        proc = subprocess.Popen(run_args, stdout=None, stderr=subprocess.STDOUT)

        while proc.poll() is None:
            time.sleep(60)
    else:
        run_args = [
            ProcessManager.gunicorn,
            "app.main:app",
            "--bind",
            f"{host}:{port}",
            "--workers",
            f"{workers}",
            "--worker-class",
            "uvicorn.workers.UvicornWorker",
        ]
        proc = subprocess.Popen(run_args, stdout=None, stderr=subprocess.STDOUT)

        while proc.poll() is None:
            time.sleep(60)


if __name__ == "__main__":
    app()
