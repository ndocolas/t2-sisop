from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class FitStrategy(ABC):
    @abstractmethod
    def select(self, free_segments: List[Tuple[int, int]], size: int, cursor: int) -> Optional[int]:
        pass

    @abstractmethod
    def update_cursor(self, chosen_start: Optional[int], chosen_size: Optional[int], current_cursor: int) -> int:
        pass


class BestFit(FitStrategy):
    def select(self, free_segments: List[Tuple[int, int]], size: int, cursor: int) -> Optional[int]:
        candidates = [segment for segment in free_segments if segment[1] >= size]
        if not candidates:
            return None
        best = min(candidates, key=lambda segment: segment[1])
        return best[0]

    def update_cursor(self, chosen_start: Optional[int], chosen_size: Optional[int], current_cursor: int) -> int:
        return current_cursor


class CircularFit(FitStrategy):
    def select(self, free_segments: List[Tuple[int, int]], size: int, cursor: int) -> Optional[int]:
        if not free_segments:
            return None

        ordered = sorted(free_segments, key=lambda seg: seg[0])
        starts = [start for start, _ in ordered]

        pivot_index = 0
        for i, start in enumerate(starts):
            if start >= cursor:
                pivot_index = i
                break

        scan_order = ordered[pivot_index:] + ordered[:pivot_index]
        for start, length in scan_order:
            if length >= size:
                return start
        return None

    def update_cursor(self, chosen_start: Optional[int], chosen_size: Optional[int], current_cursor: int) -> int:
        if chosen_start is None or chosen_size is None:
            return current_cursor
        return chosen_start + chosen_size


class FirstFit(FitStrategy):
    def select(self, free_segments: List[Tuple[int, int]], size: int, cursor: int) -> Optional[int]:
        for start, length in free_segments:
            if length >= size:
                return start
        return None

    def update_cursor(self, chosen_start: Optional[int], chosen_size: Optional[int], current_cursor: int) -> int:
        return current_cursor


class WorstFit(FitStrategy):
    def select(self, free_segments: List[Tuple[int, int]], size: int, cursor: int) -> Optional[int]:
        candidates = [segment for segment in free_segments if segment[1] >= size]
        if not candidates:
            return None
        worst = max(candidates, key=lambda segment: segment[1])
        return worst[0]

    def update_cursor(self, chosen_start: Optional[int], chosen_size: Optional[int], current_cursor: int) -> int:
        return current_cursor
