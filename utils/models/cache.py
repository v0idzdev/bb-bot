from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True, repr=True)
class Cache:
    blacklist: dict = field(default_factory=dict)
    reactionroles: dict = field(default_factory=dict)