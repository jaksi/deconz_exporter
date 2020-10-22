from dataclasses import dataclass
from typing import Any, Type, TypeVar, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Device:
    id: str
    internalipaddress: str
    macaddress: str
    internalport: int
    name: str
    publicipaddress: str

    @staticmethod
    def from_dict(obj: Any) -> "Device":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        internalipaddress = from_str(obj.get("internalipaddress"))
        macaddress = from_str(obj.get("macaddress"))
        internalport = from_int(obj.get("internalport"))
        name = from_str(obj.get("name"))
        publicipaddress = from_str(obj.get("publicipaddress"))
        return Device(id, internalipaddress, macaddress, internalport, name, publicipaddress)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["internalipaddress"] = from_str(self.internalipaddress)
        result["macaddress"] = from_str(self.macaddress)
        result["internalport"] = from_int(self.internalport)
        result["name"] = from_str(self.name)
        result["publicipaddress"] = from_str(self.publicipaddress)
        return result


def device_from_dict(s: Any) -> Device:
    return Device.from_dict(s)


def device_to_dict(x: Device) -> Any:
    return to_class(Device, x)
