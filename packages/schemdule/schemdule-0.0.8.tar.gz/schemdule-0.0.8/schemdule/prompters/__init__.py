from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Iterable, Iterator, List, Optional, Union, cast


class PromptResult(Enum):
    """Result for prompting."""
    Empty = 0
    Unsupported = 1     # Unsupported, skip this and go next
    Resolved = 2        # Resolved, go next
    Finished = 3        # Resolved, stop going next
    Failed = 4          # Failed, stop going next


class PrompterPayload(ABC):
    """Payload for prompters."""
    pass


@dataclass
class CyclePayload(PrompterPayload):
    """Payload for cycle event."""
    work: bool
    index: int


@dataclass
class UserPayload(PrompterPayload):
    """Payload that user provided."""
    payload: Any


@dataclass
class SchedulePayload(PrompterPayload):
    """Payload for scheduler information."""
    index: int
    message: str
    startTime: datetime
    endTime: datetime
    duration: timedelta = field(init=False)

    def __post_init__(self) -> None:
        self.duration = self.endTime - self.startTime


class PrompterPayloadCollection(PrompterPayload):
    """A collection for multiple payloads."""

    def __init__(self, payloads: Optional[List[PrompterPayload]] = None) -> None:
        super().__init__()
        self.payloads = payloads if payloads is not None else []

    def withPayload(self, payload: PrompterPayload) -> "PrompterPayloadCollection":
        self.payloads.append(payload)
        return self

    def withPayloads(self, payloads: "PrompterPayloadCollection") -> "PrompterPayloadCollection":
        self.payloads.extend(payloads)
        return self

    def tryGet(self, type: type) -> Iterable[PrompterPayload]:
        for item in self.payloads:
            if isinstance(item, type):
                yield item

    def getSchedule(self) -> Optional[SchedulePayload]:
        return next(iter(self.tryGet(SchedulePayload)), None)

    def getCycle(self) -> Optional[CyclePayload]:
        return next(iter(self.tryGet(CyclePayload)), None)

    def getUsers(self) -> Iterable[UserPayload]:
        return self.tryGet(UserPayload)

    def __iter__(self) -> Iterator[PrompterPayload]:
        return iter(self.payloads)

    def __repr__(self) -> str:
        return f"PrompterPayloadCollection({len(self.payloads)} payloads: {'; '.join([str(x) for x in self.payloads])})"

    def __str__(self) -> str:
        return f"Payloads({len(self.payloads)}: {'; '.join([type(x).__name__ for x in self.payloads])})"


class Prompter(ABC):
    """Prompter for every event."""

    def __init__(self, final: bool = False) -> None:
        self.final = final

    def success(self) -> PromptResult:
        return PromptResult.Finished if self.final else PromptResult.Resolved

    @abstractmethod
    def prompt(self, payloads: PrompterPayloadCollection) -> PromptResult:
        pass

    def __repr__(self) -> str:
        return type(self).__name__


class PrompterHub(Prompter, ABC):
    """Hub for multiple prompters."""
    @abstractmethod
    def register(self, prompter: Prompter) -> None:
        pass
