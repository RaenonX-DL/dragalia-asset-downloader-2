# dragalia-asset-downloader-2

[![downloader-ci]][downloader-ci-link]
[![downloader-cq-badge]][downloader-cq-link]
[![downloader-lgtm-alert-badge]][downloader-lgtm-alert-link]
[![downloader-lgtm-quality-badge]][downloader-lgtm-quality-link]
[![downloader-lgtm-loc-badge]][downloader-lgtm-quality-link]
[![downloader-time-badge]][downloader-time-link]

Python scripts for downloading and pre-processing Dragalia Lost game assets.

Replaces [dragalia-asset-downloader].

## Prerequisites

- Python 3.9

- .NET Core 3.1+
  - Download here: https://dotnet.microsoft.com/download/dotnet-core/3.1.
  - Run `dotnet` to ensure it's working.

- Dependencies listed in `requirements.txt`
  - Run `pip install -r requirements.txt` to install required dependencies.
  - Run `pip install -r requirements-dev.txt` to install required and development dependencies.

## Development

- Before commit, it is recommended to run `precommit.ps1`. Note that this created under Powershell 5.1.

[dragalia-asset-downloader]: https://github.com/RaenonX-DL/dragalia-asset-downloader

[downloader-ci]: https://github.com/RaenonX-DL/dragalia-asset-downloader-2/workflows/CI/badge.svg

[downloader-ci-link]: https://github.com/RaenonX-DL/dragalia-asset-downloader-2/actions?query=workflow%3ACI

[downloader-cq-badge]: https://app.codacy.com/project/badge/Grade/455468d9c9184f88af1249e82cb2c4ad

[downloader-cq-link]: https://www.codacy.com/gh/RaenonX-DL/dragalia-asset-downloader-2/dashboard

[downloader-time-badge]: https://wakatime.com/badge/github/RaenonX-DL/dragalia-asset-downloader-2.svg

[downloader-time-link]: https://wakatime.com/badge/github/RaenonX-DL/dragalia-asset-downloader-2

[downloader-lgtm-alert-badge]: https://img.shields.io/lgtm/alerts/g/RaenonX-DL/dragalia-asset-downloader-2.svg?logo=lgtm&logoWidth=18

[downloader-lgtm-alert-link]: https://lgtm.com/projects/g/RaenonX-DL/dragalia-asset-downloader-2/alerts/

[downloader-lgtm-quality-badge]: https://img.shields.io/lgtm/grade/python/g/RaenonX-DL/dragalia-asset-downloader-2.svg?logo=lgtm&logoWidth=18

[downloader-lgtm-quality-link]: https://lgtm.com/projects/g/RaenonX-DL/dragalia-asset-downloader-2/context:python

[downloader-lgtm-loc-badge]: https://badgen.net/lgtm/lines/g/RaenonX-DL/dragalia-asset-downloader-2
