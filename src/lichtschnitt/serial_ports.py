"""Read-only Erkennung von USB-Seriellgeräten unter Linux.

Dieses Modul öffnet keine Gerätepfade und sendet keine Bytes. Es liest nur
Dateinamen, Symlinks, Dateirechte und USB-Metadaten aus sysfs.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


@dataclass(frozen=True)
class SerialPort:
    """Beschreibende Informationen zu einem erkannten Gerät."""

    path: str
    stable_path: str | None
    vendor_id: str | None
    product_id: str | None
    manufacturer: str | None
    product: str | None
    can_read: bool
    can_write: bool

    @property
    def key(self) -> str:
        """Stabile Vergleichskennung für An- und Absteckereignisse."""
        return self.stable_path or self.path


def enumerate_ports(
    dev_root: Path = Path("/dev"),
    by_id_root: Path = Path("/dev/serial/by-id"),
    sys_root: Path = Path("/sys/class/tty"),
) -> list[SerialPort]:
    """Erkennt USB-Seriellgeräte, ohne sie zu öffnen oder anzusprechen."""
    aliases: dict[Path, str] = {}
    if by_id_root.is_dir():
        for alias in sorted(by_id_root.iterdir()):
            try:
                target = alias.resolve(strict=True)
            except (OSError, RuntimeError):
                continue
            aliases.setdefault(target, str(alias))

    device_paths: set[Path] = set()
    for pattern in ("ttyUSB*", "ttyACM*"):
        device_paths.update(dev_root.glob(pattern))

    ports: list[SerialPort] = []
    for device_path in sorted(device_paths, key=lambda item: item.name):
        vendor_id, product_id, manufacturer, product = _read_usb_metadata(
            sys_root / device_path.name / "device"
        )
        resolved_path = _resolve_without_failure(device_path)
        ports.append(
            SerialPort(
                path=str(device_path),
                stable_path=aliases.get(resolved_path),
                vendor_id=vendor_id,
                product_id=product_id,
                manufacturer=manufacturer,
                product=product,
                can_read=os.access(device_path, os.R_OK),
                can_write=os.access(device_path, os.W_OK),
            )
        )
    return ports


def _resolve_without_failure(path: Path) -> Path:
    try:
        return path.resolve(strict=True)
    except (OSError, RuntimeError):
        return path


def _read_usb_metadata(
    device_link: Path,
) -> tuple[str | None, str | None, str | None, str | None]:
    """Liest VID/PID, Hersteller und Produkt; USB-Seriennummer wird ausgelassen."""
    try:
        current = device_link.resolve(strict=True)
    except (OSError, RuntimeError):
        return None, None, None, None

    for candidate in (current, *current.parents):
        vendor_id = _read_attribute(candidate / "idVendor")
        product_id = _read_attribute(candidate / "idProduct")
        if vendor_id and product_id:
            return (
                vendor_id,
                product_id,
                _read_attribute(candidate / "manufacturer"),
                _read_attribute(candidate / "product"),
            )
    return None, None, None, None


def _read_attribute(path: Path) -> str | None:
    try:
        value = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError):
        return None
    return value or None


def format_port(port: SerialPort) -> str:
    """Formatiert einen Gerätefund für das Terminal."""
    lines = [port.path]
    if port.stable_path:
        lines.append(f"  stabiler Pfad: {port.stable_path}")
    if port.vendor_id and port.product_id:
        lines.append(f"  USB-ID: {port.vendor_id}:{port.product_id}")
    label = " ".join(value for value in (port.manufacturer, port.product) if value)
    if label:
        lines.append(f"  Gerät: {label}")
    lines.append(
        "  Dateizugriff: "
        f"Lesen {'ja' if port.can_read else 'nein'}, "
        f"Schreiben {'ja' if port.can_write else 'nein'}"
    )
    return "\n".join(lines)


def compare_ports(
    previous: Iterable[SerialPort], current: Iterable[SerialPort]
) -> tuple[list[SerialPort], list[SerialPort]]:
    """Gibt neu erkannte und entfernte Geräte in sortierbarer Form zurück."""
    previous_by_key = {port.key: port for port in previous}
    current_by_key = {port.key: port for port in current}
    added = [current_by_key[key] for key in current_by_key.keys() - previous_by_key.keys()]
    removed = [previous_by_key[key] for key in previous_by_key.keys() - current_by_key.keys()]
    return sorted(added, key=lambda port: port.key), sorted(removed, key=lambda port: port.key)


def watch_ports(
    interval: float = 1.0,
    scanner: Callable[[], list[SerialPort]] = enumerate_ports,
    sleeper: Callable[[float], None] = time.sleep,
    write: Callable[[str], None] = print,
) -> None:
    """Beobachtet Geräteänderungen, ohne serielle Verbindungen zu öffnen."""
    if interval <= 0:
        raise ValueError("Das Beobachtungsintervall muss größer als 0 sein.")

    previous = scanner()
    write("Beobachte USB-Seriellgeräte. Beenden mit Strg+C.")
    if previous:
        write("Bereits vorhanden:")
        for port in previous:
            write(format_port(port))
    else:
        write("Noch kein passendes Gerät erkannt.")

    while True:
        sleeper(interval)
        current = scanner()
        added, removed = compare_ports(previous, current)
        for port in added:
            write(f"Angesteckt:\n{format_port(port)}")
        for port in removed:
            write(f"Abgesteckt: {port.path}")
        previous = current
