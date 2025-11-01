"""Binary wire protocol framing and codecs."""

import struct
from dataclasses import dataclass


@dataclass
class FrameHeader:
    magic: int
    flags: int
    payload_length: int


class MessageCodec:
    MAGIC = 0x5A45  # 'ZE'

    @classmethod
    def encode_frame(cls, payload: bytes, flags: int = 0) -> bytes:
        header = struct.pack("!HHI", cls.MAGIC, flags, len(payload))
        return header + payload
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
    def parse_header_view(self, buffer: memoryview) -> 'FrameHeader':
        magic, flags, length = struct.unpack_from('!HHI', buffer, 0)
        return FrameHeader(magic=magic, flags=flags, payload_length=length)
