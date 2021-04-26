### Hexlet tests and linter status:
[![Actions Status](https://github.com/adryabinov/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/adryabinov/python-project-lvl3/actions)

[![Python CI](https://github.com/adryabinov/python-project-lvl3/actions/workflows/python-ci.yml/badge.svg)](https://github.com/adryabinov/python-project-lvl3/actions/workflows/python-ci.yml)

[![Maintainability](https://api.codeclimate.com/v1/badges/e0cc090c3dcbf1440e31/maintainability)](https://codeclimate.com/github/adryabinov/python-project-lvl3/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/e0cc090c3dcbf1440e31/test_coverage)](https://codeclimate.com/github/adryabinov/python-project-lvl3/test_coverage)

## Installation

Python packaging and dependency management tool Poetry should be preinstalled.

```bash
make build
make package-install
```

[![asciicast](https://asciinema.org/a/oPPxfhLS7TcJdXrnYa1ehzHEC.svg)](https://asciinema.org/a/oPPxfhLS7TcJdXrnYa1ehzHEC)

## Testing

```bash
make install
make lint
make test
```

## Usage
```bash
page-loader [-h] [-o OUTPUT] url

Downloads html page with  resources

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output folder path
```
## Working sample

### download page

[![asciicast](https://asciinema.org/a/mn3XpRgekVEiT7YgTCzxAcSrV.svg)](https://asciinema.org/a/mn3XpRgekVEiT7YgTCzxAcSrV)

### exception handling

[![asciicast](https://asciinema.org/a/ySLGn7clwyCqSRYmLSorhECHm.svg)](https://asciinema.org/a/ySLGn7clwyCqSRYmLSorhECHm)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT]
