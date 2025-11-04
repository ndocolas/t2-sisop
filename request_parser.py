from typing import List


class Request:
    def __init__(self, kind: str, pid: str | None, size: int | None):
        self.kind = kind
        self.pid = pid
        self.size = size


class RequestParser:
    def parse_file(self, path: str) -> List[Request]:
        lines: List[str] = []
        with open(path, "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                lines.append(line)
        return [self.parse_line(line) for line in lines]

    def parse_line(self, line: str) -> Request:
        text = line.strip()
        upper = text.upper()

        if upper.startswith("IN(") and text.endswith(")"):
            content = text[3:-1]
            parts = [part.strip() for part in content.split(",")]
            if len(parts) != 2:
                raise ValueError(f"Linha inválida: {line}")
            pid, size_str = parts
            size = int(size_str)
            return Request("IN", pid, size)

        if upper.startswith("OUT(") and text.endswith(")"):
            pid = text[4:-1].strip()
            return Request("OUT", pid, None)

        if text.isdigit():
            value = int(text)
            return Request("MEM", None, value)

        raise ValueError(f"Linha inválida: {line}")
