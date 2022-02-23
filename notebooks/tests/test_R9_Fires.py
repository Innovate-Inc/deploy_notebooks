from notebooks.func import format_global, compare_ids

print('testing here')


def test_format_global():
    # from R9_FiresNotebookDeploy_clean import format_global
    assert format_global('123oiuTTTB', braces=True) == '{123oiuTTTB}'
    assert format_global('123oiuTTTB', braces=False) == '123oiuTTTB'
    assert format_global('{aaBBCCdd123!}', braces=False) == 'aaBBCCdd123!'
    assert format_global('{aaBBCCdd123!}', braces=True) == '{aaBBCCdd123!}'


def test_compare_ids():
    assert compare_ids('12332', None) is False
    assert compare_ids('12332', '{12332}') is True
    assert compare_ids('123123', '234234') is False
    assert compare_ids('73d60991-9df6-4153-aa3b-537961ecbfb8', '73d60991-9df6-4153-aa3b-537961ecbfb8') is True
    assert compare_ids('{73d60991-9df6-4153-aa3b-537961ecbfb8}', '73d60991-9df6-4153-aa3b-537961ecbfb8') is True
