import os
from pathlib import Path
from bs4 import BeautifulSoup
from page_loader.comparator import soup
from page_loader.comparator import replace_img


FIXTURES_DIR = 'fixtures'


def make_path(file_name):
    dir_path = Path(__file__).absolute().parent
    return os.path.join(dir_path, FIXTURES_DIR, file_name)


def open_file(path):
    with open(path) as f:
        return f.read()


soup = BeautifulSoup(open_file(make_path('replace_img_test.html')))
out_soup = BeautifulSoup(open_file(make_path('replace_img_test_replaced.html')))

def test_replace_img():
    assert replace_img(soup, 'some-domain.ru') == out_soup