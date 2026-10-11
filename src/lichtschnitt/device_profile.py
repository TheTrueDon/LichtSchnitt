"""Laden und prüfen eines LichtSchnitt-Geräteprofils."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProfileError(ValueError):
    """Das Profil fehlt oder enthält ungültige bzw. widersprüchliche Werte."""


def load_profile(path: str | Path) -> dict[str, Any]:
    """Lädt ein JSON-Profil und validiert die v1-Profilstruktur."""
    profile_path = Path(path)
    try:
        with profile_path.open("r", encoding="utf-8") as profile_file:
            profile = json.load(profile_file)
    except FileNotFoundError as exc:
        raise ProfileError(f"Profil nicht gefunden: {profile_path}") from exc
    except json.JSONDecodeError as exc:
        raise ProfileError(f"Profil enthält ungültiges JSON: {profile_path}") from exc

    validate_profile(profile)
    return profile


def validate_profile(profile: Any) -> None:
    """Prüft die bekannten Pflichtfelder, ohne unbekannte Werte zu erraten."""
    if not isinstance(profile, dict):
        raise ProfileError("Profil muss ein JSON-Objekt sein.")

    required_text = (
        "profile_schema_version",
        "profile_id",
        "machine_name",
        "controller_name",
        "firmware_reported",
        "connection",
        "protocol_family_expected",
    )
    for key in required_text:
        value = profile.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ProfileError(f"Pflichtfeld fehlt oder ist leer: {key}")

    if profile["profile_schema_version"] != "1":
        raise ProfileError("Nicht unterstützte Profilstrukturversion.")

    workspace = profile.get("workspace_mm")
    if (
        not isinstance(workspace, dict)
        or not _is_positive_number(workspace.get("width"))
        or not _is_positive_number(workspace.get("height"))
    ):
        raise ProfileError("Arbeitsbereich muss positive Breite und Höhe in mm enthalten.")

    laser = profile.get("laser_module")
    if not isinstance(laser, dict):
        raise ProfileError("Angaben zum Lasermodul fehlen.")
    for key in ("wavelength_nm", "optical_power_w", "max_input_voltage_v", "max_input_current_a"):
        pair = laser.get(key)
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or not all(_is_positive_number(value) for value in pair)
            or pair[0] > pair[1]
        ):
            raise ProfileError(f"Ungültiger Wertebereich im Lasermodul: {key}")

    interface = profile.get("serial_interface")
    if not isinstance(interface, dict):
        raise ProfileError("Angaben zur seriellen Schnittstelle fehlen.")
    if interface.get("baud_rate") is not None:
        raise ProfileError("Baudrate muss offen bleiben, bis sie am Gerät geprüft wurde.")
    if interface.get("laser_commands_enabled") is not False:
        raise ProfileError("Laserbefehle müssen im Geräteprofil deaktiviert bleiben.")


def _is_positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0
