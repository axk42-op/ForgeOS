"""Generate forge.ico from the anvil emblem (stdlib only)."""

from __future__ import annotations

import struct
from pathlib import Path


def _draw_icon(size: int) -> list[tuple[int, int, int, int]]:
    """Return RGBA pixels, row-major top-down."""
    bg = (13, 17, 23, 255)
    orange = (255, 140, 0, 255)
    spark = (255, 179, 71, 255)
    anvil1 = (74, 88, 102, 255)
    anvil2 = (61, 74, 86, 255)
    anvil3 = (86, 102, 116, 255)

    pixels = [bg] * (size * size)

    def set_px(x: int, y: int, color: tuple[int, int, int, int]) -> None:
        if 0 <= x < size and 0 <= y < size:
            pixels[y * size + x] = color

    def fill_rect(x0: int, y0: int, x1: int, y1: int, color) -> None:
        for y in range(y0, y1):
            for x in range(x0, x1):
                set_px(x, y, color)

    def fill_circle(cx: int, cy: int, r: int, color) -> None:
        r2 = r * r
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                    set_px(x, y, color)

    s = size / 128.0

    def sx(v: float) -> int:
        return int(v * s)

    # sparks
    fill_circle(sx(64), sx(22), max(1, sx(5)), orange)
    fill_circle(sx(52), sx(30), max(1, sx(3)), spark)
    fill_circle(sx(76), sx(30), max(1, sx(3)), spark)
    for y in range(sx(34), sx(46)):
        t = (y - sx(34)) / max(1, sx(46) - sx(34))
        half = int((1 - t) * sx(6))
        for x in range(sx(64) - half, sx(64) + half + 1):
            set_px(x, y, orange)

    fill_rect(sx(28), sx(52), sx(100), sx(64), anvil1)
    fill_rect(sx(34), sx(64), sx(94), sx(72), anvil1)
    fill_rect(sx(42), sx(72), sx(86), sx(88), anvil2)
    fill_rect(sx(54), sx(88), sx(74), sx(106), anvil2)
    fill_rect(sx(48), sx(106), sx(80), sx(114), anvil3)

    return pixels


def _bmp_payload(size: int, pixels: list[tuple[int, int, int, int]]) -> bytes:
    """ICO-embedded BMP: XOR (BGRA bottom-up) + AND mask."""
    height = size * 2
    header = struct.pack(
        "<IIIHHIIIIII",
        40,
        size,
        height,
        1,
        32,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    xor = bytearray()
    for y in range(size - 1, -1, -1):
        row = pixels[y * size : (y + 1) * size]
        for b, g, r, a in row:
            xor.extend((b, g, r, a))
        pad = (4 - (size * 4) % 4) % 4
        xor.extend(b"\x00" * pad)

    and_row_bytes = ((size + 31) // 32) * 4
    and_mask = b"\x00" * (and_row_bytes * size)
    return header + bytes(xor) + and_mask


def write_ico(path: Path, sizes: list[int]) -> None:
    images = [(size, _bmp_payload(size, _draw_icon(size))) for size in sizes]
    count = len(images)
    offset = 6 + 16 * count
    parts = [struct.pack("<HHH", 0, 1, count)]

    for size, data in images:
        parts.append(
            struct.pack(
                "<BBBBHHII",
                size if size < 256 else 0,
                size if size < 256 else 0,
                0,
                0,
                1,
                32,
                len(data),
                offset,
            )
        )
        offset += len(data)

    for _, data in images:
        parts.append(data)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(parts))


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    targets = [
        root / "assets" / "icons" / "forge.ico",
        root / "desktop" / "assets" / "icons" / "forge.ico",
    ]
    for out in targets:
        write_ico(out, [16, 32, 48, 64, 128, 256])
        print(f"Wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
