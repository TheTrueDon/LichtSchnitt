"""Kommandozeilen-Einstieg für die frühe Projektversion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lichtschnitt import __version__
from lichtschnitt.device_profile import load_profile


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
        choices=("version", "profil"),
        default="version",
        help="version zeigt die Programmversion; profil zeigt das Zielgerät.",
    )
    args = parser.parse_args()

    if args.command == "version":
        print(f"LichtSchnitt v{__version__}")
        print("Projektgrundlage; keine Verbindung zum Laser wird geöffnet.")
        return

    profile = load_profile(PROFILE_PATH)
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    print("\nNur Profilanzeige: keine USB-Verbindung und keine Maschinensteuerung.")


if __name__ == "__main__":
    main()
