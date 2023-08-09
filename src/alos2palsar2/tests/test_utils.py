from shared.utils import build_alos2palsar2_metadata

def test_build_metadata(alos2palsar2_summary_fp):

    metadata = build_alos2palsar2_metadata(metadata_fp=alos2palsar2_summary_fp)

    assert False