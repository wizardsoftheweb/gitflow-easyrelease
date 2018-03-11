# pylint: disable=missing-docstring

from pytest import mark

from gitflow_easyrelease import is_semver


@mark.parametrize(
    "version,expected",
    [
        ('v0.0.0', True),
        ('0.0.0', True),
        ('v1.2.3', True),
        ('1.2.3', True),
        ('vX.Y.Z', False),
        ('X.Y.Z', False),
        ('vqqq', False),
        ('qqq', False),
    ]
)
def test_is_semver(version, expected):
    assert expected == is_semver(version)
