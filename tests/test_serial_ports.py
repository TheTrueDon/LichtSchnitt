"""Isolierte Tests der Linux-Port-Erkennung ohne Hardwarezugriff."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from lichtschnitt.serial_ports import SerialPort, compare_ports, enumerate_ports, format_port


class SerialPortTests(unittest.TestCase):
    def test_enumerates_usb_serial_nodes_and_stable_by_id_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            dev_root = root / "dev"
            by_id_root = dev_root / "serial" / "by-id"
            sys_root = root / "sys" / "class" / "tty"
            usb_parent = root / "sys" / "devices" / "usb1" / "1-2"
            dev_root.mkdir(parents=True)
            by_id_root.mkdir(parents=True)
            (sys_root / "ttyUSB0").mkdir(parents=True)
            usb_parent.mkdir(parents=True)

            (dev_root / "ttyUSB0").touch()
            (dev_root / "ttyACM0").touch()
            (dev_root / "ttyS0").touch()
            (usb_parent / "idVendor").write_text("1a86\n", encoding="utf-8")
            (usb_parent / "idProduct").write_text("7523\n", encoding="utf-8")
            (usb_parent / "manufacturer").write_text("USB Serial", encoding="utf-8")
            (usb_parent / "product").write_text("Controller", encoding="utf-8")
            (sys_root / "ttyUSB0" / "device").symlink_to(usb_parent)
            (by_id_root / "usb-USB_Serial-if00-port0").symlink_to(dev_root / "ttyUSB0")

            ports = enumerate_ports(dev_root, by_id_root, sys_root)

            expected = [str(dev_root / "ttyACM0"), str(dev_root / "ttyUSB0")]
            self.assertEqual([port.path for port in ports], expected)
            usb_port = next(port for port in ports if port.path.endswith("ttyUSB0"))
            self.assertEqual(usb_port.stable_path, str(by_id_root / "usb-USB_Serial-if00-port0"))
            self.assertEqual((usb_port.vendor_id, usb_port.product_id), ("1a86", "7523"))
            self.assertEqual((usb_port.manufacturer, usb_port.product), ("USB Serial", "Controller"))

    def test_compare_ports_reports_added_and_removed(self) -> None:
        old = SerialPort("/dev/ttyUSB0", "/dev/serial/by-id/laser", None, None, None, None, True, True)
        new = SerialPort("/dev/ttyACM0", "/dev/serial/by-id/laser", None, None, None, None, True, True)
        extra = SerialPort("/dev/ttyUSB1", None, None, None, None, None, True, True)

        added, removed = compare_ports([old], [new, extra])

        self.assertEqual([port.path for port in added], ["/dev/ttyUSB1"])
        self.assertEqual(removed, [])

    def test_format_reports_file_permissions(self) -> None:
        port = SerialPort("/dev/ttyUSB0", "/dev/serial/by-id/usb-device", "1a86", "7523", "Maker", "Controller", True, False)

        output = format_port(port)

        self.assertIn("Dateizugriff: Lesen ja, Schreiben nein", output)
        self.assertIn("1a86:7523", output)

    def test_only_scans_usb_serial_device_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            dev_root = Path(temporary_directory) / "dev"
            dev_root.mkdir()
            (dev_root / "ttyS0").touch()
            (dev_root / "ttyUSB0").touch()

            ports = enumerate_ports(dev_root, dev_root / "by-id", Path(temporary_directory) / "sys")

            self.assertEqual([port.path for port in ports], [str(dev_root / "ttyUSB0")])


if __name__ == "__main__":
    unittest.main()
