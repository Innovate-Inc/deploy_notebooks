cleaned = __import__('R9_FiresNotebookDeploy_clean')
print('testing here')

def test_format_global():
    # from R9_FiresNotebookDeploy_clean import format_global
    assert cleaned.format_global('123oiuTTTB', braces=True) == '{123oiuTTTB}'
    assert cleaned.format_global('123oiuTTTB', braces=False) == '123oiuTTTB'
    assert cleaned.format_global('{aaBBCCdd123!}', braces=False) == 'aaBBCCdd123!'
    assert cleaned.format_global('{aaBBCCdd123!}', braces=True) == '{aaBBCCdd123!}'
