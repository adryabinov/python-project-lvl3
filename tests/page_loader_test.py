from page_loader.comparator import download

def test_loader_output():
    file_path = download(
        'https://ru.hexlet.io/courses', '/var/tmp'
    )
    assert file_path == '/var/tmp/ru-hexlet-io-courses.html'
