"""GPU information commands."""

from ._helpers import current_os, run, section


def _gpu_windows():
    output = run(["wmic", "path", "win32_VideoController", "get", "Name,AdapterRAM,DriverVersion"])
    if output:
        print(output)
    else:
        print("  No GPU information available via wmic.")


def _gpu_linux():
    found = False

    lspci = run(["lspci"])
    if lspci:
        gpu_lines = [
            line for line in lspci.splitlines()
            if "VGA" in line or "3D" in line or "Display" in line
        ]
        if gpu_lines:
            print("  Detected GPUs (lspci):")
            for line in gpu_lines:
                print(f"    {line}")
            found = True

    nvidia = run([
        "nvidia-smi",
        "--query-gpu=name,driver_version,memory.total,memory.free,utilization.gpu",
        "--format=csv,noheader,nounits",
    ])
    if nvidia:
        print()
        print("  NVIDIA GPU Details (nvidia-smi):")
        headers = ["Name", "Driver", "Total VRAM (MiB)", "Free VRAM (MiB)", "GPU Util%"]
        rows = [r.split(", ") for r in nvidia.splitlines()]
        col_w = [
            max(len(h), max((len(r[i]) for r in rows if i < len(r)), default=0))
            for i, h in enumerate(headers)
        ]
        header_line = "  " + "  ".join(h.ljust(col_w[i]) for i, h in enumerate(headers))
        print(header_line)
        print("  " + "-" * (len(header_line) - 2))
        for row_data in rows:
            print(
                "  "
                + "  ".join(
                    (row_data[i] if i < len(row_data) else "").ljust(col_w[i])
                    for i in range(len(headers))
                )
            )
        found = True

    if not found:
        print("  No GPU information found. Ensure lspci or nvidia-smi is installed.")


def _gpu_macos():
    output = run(["system_profiler", "SPDisplaysDataType"])
    if output:
        for line in output.splitlines():
            stripped = line.strip()
            if stripped:
                print(f"  {stripped}")
    else:
        print("  No GPU information available via system_profiler.")


def gpu(args):
    """Display GPU information (OS-aware).

    Usage: gpu
    """
    section("GPU Information")
    os_name = current_os()

    try:
        if os_name == "windows":
            _gpu_windows()
        elif os_name == "darwin":
            _gpu_macos()
        else:
            _gpu_linux()
    except Exception as exc:
        print(f"[gpu] Error: {exc}")
