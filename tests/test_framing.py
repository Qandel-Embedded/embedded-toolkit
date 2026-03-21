from embedded_toolkit import FrameEncoder, FrameDecoder


def roundtrip(data):
    enc = FrameEncoder()
    dec = FrameDecoder()
    frame = enc.encode(data)
    result = None
    for b in frame:
        result = dec.feed(b)
        if result is not None:
            break
    return result


def test_simple_roundtrip():
    assert roundtrip(b'hello') == b'hello'


def test_escape_flag_byte():
    assert roundtrip(bytes([0x7E, 0x01, 0x7D])) == bytes([0x7E, 0x01, 0x7D])


def test_empty_payload():
    assert roundtrip(b'') == b''


def test_binary_data():
    data = bytes(range(256))
    assert roundtrip(data) == data
