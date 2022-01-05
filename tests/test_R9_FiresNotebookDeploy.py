from arcgis.geometry import Point, Polygon
import os


def pytest_sessionstart(session):
    print('BEFORE')
    from update_ipynb import clean_py_script
    clean_py_script(os.path.basename(__file__))
def test_buffer_miles():
    p = Point({"x" : -118.15, "y" : 33.80, "spatialReference" : {"wkid" : 4326}})
    cleaned = __import__('R9_FiresNotebookDeploy_clean')
    buffer_10 = cleaned.buffer_miles(p, in_wkid = 4326)
    assert isinstance(buffer_10, Polygon)
