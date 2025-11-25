from interpreter import RequestParser
from memory_manager import MemoryManager
from fit_strategy import FitStrategy


class Simulator:
    def __init__(self, policy: FitStrategy):
        self.policy = policy
        self.manager: MemoryManager | None = None

    def run(self, script_path: str, initial_size: int) -> None:
        parser = RequestParser()
        requests = parser.parse_file(script_path)

        memory_size = initial_size

        self.manager = MemoryManager(memory_size, self.policy)
        self.print_memory_map("Inicial")

        for request in requests:
            cmd_text = self.format_command(request)

            if request.kind == "IN":
                if request.pid is None:
                    print(f"{cmd_text} → PID INVÁLIDO")
                    continue
                if request.size is None:
                    print(f"{cmd_text} → TAMANHO INVÁLIDO")
                    continue
                allocated = self.manager.allocate(request.pid, request.size)
                if not allocated:
                    print(f"{cmd_text} → ESPAÇO INSUFICIENTE DE MEMÓRIA")
                    continue
            elif request.kind == "OUT":
                if request.pid is None:
                    print(f"{cmd_text} → PID INVÁLIDO")
                    continue
                self.manager.release(request.pid)

            self.print_memory_map(cmd_text)

    def format_command(self, request) -> str:
        if request.kind == "IN":
            return f"IN({request.pid},{request.size})"
        elif request.kind == "OUT":
            return f"OUT({request.pid})"
        return "CMD"

    def print_memory_map(self, command: str) -> None:
        if self.manager is None:
            return
        snapshot = self.manager.segments_snapshot()
        if not snapshot:
            print(f"{command} → [ Empty ]")
            return

        parts = []
        for _, size, pid in snapshot:
            label = pid if pid is not None else "Free"
            parts.append(f"[ {label} - {size} ]")

        formatted = " ".join(parts)
        print(f"{command} → {formatted}")

    def is_power_of_two(self, x: int) -> bool:
        return x > 0 and (x & (x - 1)) == 0
