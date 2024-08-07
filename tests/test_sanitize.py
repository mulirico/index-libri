from index_libri.sanitize import sanitize


def test_sanitize_strings():
    string_suja = 'Abacaxi!@ Banana    CAJU??'
    string_sanitizada = sanitize(string_suja)

    assert string_sanitizada == 'abacaxi banana caju'
