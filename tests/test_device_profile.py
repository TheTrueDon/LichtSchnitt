"""Prüfungen der Geräteprofildaten aus v0.0.1."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from lichtschnitt.device_profile import ProfileError, load_profile, validate_profile


PROFILE_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "lichtschnitt"
    / "profiles"
    / "longer_ray5_10w_mks_dlc32_v2_1.json"
)


class DeviceProfileTests(unittest.TestCase):
    def test_target_profile_loads_with_reported_machine_values(self) -> None:
        profile = load_profile(PROFILE_PATH)

        self.assertEqual(profile["machine_name"], "Longer RAY5 10W")
        self.assertEqual(profile["workspace_mm"], {"width": 400, "height": 400})
        self.assertEqual(profile["controller_name"], "MKS DLC32 V2.1")
        self.assertEqual(profile["firmware_reported"], "V2.20 (8M.H35.20230626)")

    def test_unknown_interface_values_stay_unset_and_outputs_disabled(self) -> None:
        profile = load_profile(PROFILE_PATH)

        self.assertIsNone(profile["serial_interface"]["baud_rate"])
        self.assertFalse(profile["serial_interface"]["laser_commands_enabled"])
        self.assertFalse(profile["serial_interface"]["motion_commands_enabled"])
        self.assertFalse(profile["verification"]["verified_on_device"])

    def test_profile_rejects_a_guessed_baud_rate(self) -> None:
        profile = load_profile(PROFILE_PATH)
        profile["serial_interface"]["baud_rate"] = 115200

        with self.assertRaises(ProfileError):
            validate_profile(profile)

    def test_profile_rejects_non_positive_workspace(self) -> None:
        profile = load_profile(PROFILE_PATH)
        profile["workspace_mm"]["width"] = 0

        with self.assertRaises(ProfileError):
            validate_profile(profile)

    def test_invalid_json_is_reported_as_profile_error(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            bad_profile = Path(temporary_directory) / "bad.json"
            bad_profile.write_text("{", encoding="utf-8")

            with self.assertRaises(ProfileError):
                load_profile(bad_profile)


if __name__ == "__main__":
    unittest.main()
