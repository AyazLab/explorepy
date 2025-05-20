from unittest.mock import patch

import pytest

import explorepy


# Fixture for common setup
@pytest.fixture
def mock_explore():
    explorepy.set_bt_interface('mock')
    explore = explorepy.Explore()
    explore.connect(device_name='Explore_1C35')
    return explore


def test_channel_name_setting(mock_explore):
    """Test that channel names are set correctly"""
    # Set channel names
    mock_explore.set_exg_channel_name(1, 'Pz')
    mock_explore.set_exg_channel_name(2, 'Cz')

    # Get the channel names
    assert mock_explore.get_exg_channel_name(1) == 'Pz'
    assert mock_explore.get_exg_channel_name(2) == 'Cz'


def test_reference_label_setting(mock_explore):
    """Test reference label configuration"""
    mock_explore.set_reference_label('Ref_Node', is_subtracted=True, is_common_average=False)

    # Assert the reference settings
    assert mock_explore.get_reference_label() == 'Ref_Node'
    assert mock_explore.is_reference_subtracted()
    assert not mock_explore.is_common_average_reference()


def test_filter_addition(mock_explore):
    """Test adding filters to the stream processor"""
    # Add notch filter
    mock_explore.stream_processor.add_filter(cutoff_freq=50, filter_type='notch')

    # Add high-pass filter
    mock_explore.stream_processor.add_filter(cutoff_freq=0.1, filter_type='highpass')

    # Add a low-pass filter
    mock_explore.stream_processor.add_filter(cutoff_freq=100, filter_type='lowpass')

    # Assert filters were added correctly
    filters = mock_explore.stream_processor.filters
    assert len(filters) == 3
    assert any(f.filter_type == 'notch' and f.cutoff_freq == 50 for f in filters)
    assert any(f.filter_type == 'highpass' and f.cutoff_freq == 0.1 for f in filters)
    assert any(f.filter_type == 'lowpass' and f.cutoff_freq == 100 for f in filters)


@patch('explorepy.Explore.push2lsl')
def test_lsl_pushing(mock_push2lsl, mock_explore):
    """Test LSL data pushing"""
    mock_explore.push2lsl(duration=5)
    mock_push2lsl.assert_called_once_with(duration=5)
