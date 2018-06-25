import attr


@attr.dataclass(frozen=True)
class ExternalWebserver:
    url: str
