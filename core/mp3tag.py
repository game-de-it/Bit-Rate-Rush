"""MP3 の ID3v2 タグから曲名 (TIT2) だけを読む最小実装 (外部ライブラリなし)。無ければ None。"""
import struct


def _syncsafe(b):
    return (b[0] << 21) | (b[1] << 14) | (b[2] << 7) | b[3]


def _decode(data):
    if not data:
        return None
    enc, body = data[0], data[1:]
    try:
        if enc == 0:
            return body.decode("latin-1").rstrip("\x00")
        if enc == 1:
            return body.decode("utf-16").rstrip("\x00")
        if enc == 2:
            return body.decode("utf-16-be").rstrip("\x00")
        return body.decode("utf-8").rstrip("\x00")
    except Exception:
        return None


def title(path):
    try:
        with open(path, "rb") as f:
            head = f.read(10)
            if head[:3] != b"ID3":
                return None
            ver = head[3]
            size = _syncsafe(head[6:10])
            data = f.read(size)
        pos = 0
        while pos + 10 <= len(data):
            fid = data[pos:pos + 4]
            if fid == b"\x00\x00\x00\x00":
                break
            if ver >= 4:
                fsize = _syncsafe(data[pos + 4:pos + 8])
            else:
                fsize = struct.unpack(">I", data[pos + 4:pos + 8])[0]
            body = data[pos + 10:pos + 10 + fsize]
            if fid == b"TIT2":
                t = _decode(body)
                return t.strip() if t else None
            pos += 10 + fsize
    except Exception:
        return None
    return None
