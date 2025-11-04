from typing import Dict, List, Tuple
from fit_strategy import FitStrategy


class MemorySegment:
    def __init__(self, start: int, size: int, pid: str | None):
        self.start = start
        self.size = size
        self.pid = pid

    def end(self) -> int:
        return self.start + self.size

    def is_free(self) -> bool:
        return self.pid is None


class MemoryManager:
    def __init__(self, total_size: int, policy: FitStrategy):
        self.total_size = total_size
        self.policy = policy
        self.segments: List[MemorySegment] = [MemorySegment(0, total_size, None)]
        self.process_index: Dict[str, MemorySegment] = {}
        self.cursor_position = 0

    def free_segments(self) -> List[Tuple[int, int]]:
        blocks: List[Tuple[int, int]] = []
        for segment in sorted(self.segments, key=lambda s: s.start):
            if segment.is_free():
                blocks.append((segment.start, segment.size))
        return blocks

    def free_block_sizes_in_order(self) -> List[int]:
        sizes: List[int] = []
        for segment in sorted(self.segments, key=lambda s: s.start):
            if segment.is_free():
                sizes.append(segment.size)
        return sizes

    def segments_snapshot(self) -> List[Tuple[int, int, str | None]]:
        ordered = sorted(self.segments, key=lambda s: s.start)
        return [(s.start, s.size, s.pid) for s in ordered]

    def allocate(self, pid: str, size: int) -> bool:
        if pid in self.process_index:
            return False

        choice_start = self.policy.select(self.free_segments(), size, self.cursor_position)
        if choice_start is None:
            return False

        target = None
        for segment in sorted(self.segments, key=lambda s: s.start):
            if segment.is_free() and segment.start == choice_start and segment.size >= size:
                target = segment
                break
        if target is None:
            return False

        if target.size == size:
            target.pid = pid
            self.process_index[pid] = target
            self.cursor_position = self.policy.update_cursor(target.start, target.size, self.cursor_position)
            return True

        new_alloc = MemorySegment(target.start, size, pid)
        new_free = MemorySegment(target.start + size, target.size - size, None)
        self.segments.remove(target)
        self.segments.extend([new_alloc, new_free])
        self.segments.sort(key=lambda s: s.start)
        self.process_index[pid] = new_alloc
        self.cursor_position = self.policy.update_cursor(new_alloc.start, new_alloc.size, self.cursor_position)
        return True

    def release(self, pid: str) -> bool:
        if pid not in self.process_index:
            return False
        segment = self.process_index.pop(pid)
        segment.pid = None
        self.coalesce()
        return True

    def coalesce(self) -> None:
        self.segments.sort(key=lambda s: s.start)
        merged: List[MemorySegment] = []
        for segment in self.segments:
            if not merged:
                merged.append(segment)
                continue
            last = merged[-1]
            if last.is_free() and segment.is_free() and last.end() == segment.start:
                last.size += segment.size
            else:
                merged.append(segment)
        self.segments = merged
        self.cursor_position = min(self.cursor_position, self.total_size)

    def total_free(self) -> int:
        return sum(segment.size for segment in self.segments if segment.is_free())
