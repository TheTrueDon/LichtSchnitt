"""Kommandozeilen-Einstieg für die frühe Projektversion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lichtschnitt import __version__
from lichtschnitt.device_profile import load_profile
from lichtschnitt.serial_ports import enumerate_ports, format_port, watch_ports


PROFILE_PATH = (
    Path(__file__).resolve().parent
    / "profiles"
    / "longer_ray5_10w_mks_dlc32_v2_1.json"
)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="lichtschnitt",
        description="Projektgrundlage für die CNC-Lasersoftware LichtSchnitt.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"LichtSchnitt v{__version__}",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("version", "profil", "ports", "watch"),
        default="version",
        help="version, profil, ports oder watch auswählen.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Abfrageintervall in Sekunden für watch (Standard: 1).",
    )
    args = parser.parse_args()

    if args.command == "version":
        print(f"LichtSchnitt v{__version__}")
        print("USB-Erkennung ohne serielle Verbindung oder Maschinensteuerung.")
        return

    if args.command == "profil":
        profile = load_profile(PROFILE_PATH)
        print(json.dumps(profile, ensure_ascii=False, indent=2))
        print("\nNur Profilanzeige: keine USB-Verbindung und keine Maschinensteuerung.")
        return

    if args.command == "ports":
        ports = enumerate_ports()
        if not ports:
            print("Keine passenden USB-Seriellgeräte gefunden.")
            print("Geprüft werden /dev/ttyUSB* und /dev/ttyACM*.")
            return
        for port in ports:
            print(format_port(port))
        print("\nNur erkannt: kein Port geöffnet, keine Bytes gesendet.")
        return

    if args.command == "watch":
        try:
            watch_ports(interval=args.interval)
        except KeyboardInterrupt:
            print("\nBeobachtung beendet. Es wurde keine Verbindung zum Laser geöffnet.")


if __name__ == "__main__":
    main()
