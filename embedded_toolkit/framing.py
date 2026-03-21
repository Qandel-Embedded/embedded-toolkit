"""HDLC-style byte framing for reliable serial communication."""

START_FLAG = 0x7E
ESCAPE     = 0x7D
XOR_KEY    = 0x20


class FrameEncoder:
    """Encode arbitrary bytes into an escaped HDLC-style frame.

    Example::

        enc = FrameEncoder()
        raw_frame = enc.encode(b'\x01\x02\x7e\x03')
        serial.write(raw_frame)
    """

    def encode(self, data: bytes) -> bytes:
        out = bytearray([START_FLAG])
        for byte in data:
            if byte in (START_FLAG, ESCAPE):
                out += bytes([ESCAPE, byte ^ XOR_KEY])
            else:
                out.append(byte)
        out.append(START_FLAG)
        return bytes(out)


class FrameDecoder:
    """Streaming HDLC-style frame decoder (feed bytes one at a time).

    Example::

        dec = FrameDecoder()
        for byte in serial_stream:
            frame = dec.feed(byte)
            if frame is not None:
                process(frame)
    """

    def __init__(self):
        self._buf     = bytearray()
        self._escape  = False
        self._in_frame = False

    def feed(self, byte: int):
        """Feed one byte. Returns decoded payload bytes or None."""
        if byte == START_FLAG:
            if self._in_frame and self._buf:
                result         = bytes(self._buf)
                self._buf      = bytearray()
                self._in_frame = False
                return result
            self._in_frame = True
            self._buf      = bytearray()
            return None

        if not self._in_frame:
            return None

        if byte == ESCAPE:
            self._escape = True
            return None

        if self._escape:
            byte ^= XOR_KEY
            self._escape = False

        self._buf.append(byte)
        return None
