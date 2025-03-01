"""Unit tests for binary framing and protocol."""

from zenith.network.protocol import MessageCodec


def test_frame_encoding():
    payload = b"test payload"
    frame = MessageCodec.encode_frame(payload)
    assert len(frame) == len(payload) + 8
