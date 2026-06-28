"""System-level commands."""

from . import (
    cpu,
    disk,
    env,
    gpu,
    memory,
    network_info,
    overview,
    packages,
    processes,
    services,
    terminal,
    uptime,
)


class SystemCommands:
    """Handles system-related shell commands."""

    clear = staticmethod(terminal.clear)
    system = staticmethod(overview.system)
    hardware = staticmethod(overview.hardware)
    cpu = staticmethod(cpu.cpu)
    memory = staticmethod(memory.memory)
    disk = staticmethod(disk.disk)
    network = staticmethod(network_info.network)
    processes = staticmethod(processes.processes)
    env = staticmethod(env.env)
    uptime = staticmethod(uptime.uptime)
    gpu = staticmethod(gpu.gpu)
    services = staticmethod(services.services)
    packages = staticmethod(packages.packages)
