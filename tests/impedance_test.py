from unittest.mock import patch
import time

import pytest
import explorepy
from explorepy.stream_processor import TOPICS
from pylsl import resolve_streams


# Fixture for common setup
@pytest.fixture
def mock_explore():
    explorepy.set_bt_interface('mock')
    explore = explorepy.Explore()
    explore.connect(device_name='Explore_1C35')
    return explore


def test_push2lsl_streams(mock_explore):
    """Test that push2lsl creates exactly the expected streams."""
    # Start streaming
    mock_explore.push2lsl(duration=10, block=False)
    
    # Give more time for streams to be created
    time.sleep(2)
    
    # Get the created streams using pylsl
    streams = resolve_streams()
    print(f"\nFound {len(streams)} streams:")
    for stream in streams:
        print(f"  - {stream.name()}")
    
    # Check that we have exactly 3 streams
    assert len(streams) == 3, f"Expected 3 streams, got {len(streams)}"
    
    # Get stream names
    stream_names = [stream.name() for stream in streams]
    
    # Check for required streams
    required_streams = [
        f"{mock_explore.device_name}_ExG",
        f"{mock_explore.device_name}_ORN",
        f"{mock_explore.device_name}_Marker"  # Using the actual name found in streams
    ]
    
    # Verify each required stream exists
    for required in required_streams:
        assert required in stream_names, f"Missing required stream: {required}"
    
    # Verify no extra streams
    assert set(stream_names) == set(required_streams), \
        f"Unexpected streams found. Expected {required_streams}, got {stream_names}"
    
    # Clean up
    mock_explore.stop_lsl()


def test_push2lsl_impedance_streams(mock_explore):
    """Test that push2lsl_impedance creates exactly the expected streams."""
    # Start streaming with impedance
    mock_explore.push2lsl_impedance(duration=10, block=False)
    
    # Give more time for streams to be created
    time.sleep(2)
    
    # Get the created streams using pylsl
    streams = resolve_streams()
    print(f"\nFound {len(streams)} streams:")
    for stream in streams:
        print(f"  - {stream.name()}")
    
    # Check that we have exactly 4 streams
    assert len(streams) == 4, f"Expected 4 streams, got {len(streams)}"
    
    # Get stream names
    stream_names = [stream.name() for stream in streams]
    
    # Check for required streams
    required_streams = [
        f"{mock_explore.device_name}_ExG",
        f"{mock_explore.device_name}_ORN",
        f"{mock_explore.device_name}_Marker",
        f"{mock_explore.device_name}_Impedance"
    ]
    
    # Verify each required stream exists
    for required in required_streams:
        assert required in stream_names, f"Missing required stream: {required}"
    
    # Verify no extra streams
    assert set(stream_names) == set(required_streams), \
        f"Unexpected streams found. Expected {required_streams}, got {stream_names}"
    
    # Clean up
    mock_explore.stop_lsl()


