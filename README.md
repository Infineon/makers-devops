<a id="readme-top"></a>



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Issues][issues-shield]][issues-url]
[![Commits][commit-shield]][commit-url]
[![Commits2][commit2-shield]][commit2-url]
[![Pull requests][pull-request-shield]][pull-request-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Documentation status][doc-status-shield]][doc-status-url]
[![MIT License][license-shield]][license-url]
[![Contributor Covenant][contributor-covenant-shield]][contributor-covenant-url]
[![Pre-commit used][pre-commit-shield]][pre-commit-url]


<!-- [![CI](https://img.shields.io/github.com/Infineon/makers-devops/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/Infineon/makers-devops/actions/workflows/build.yml)
[![CI](https://img.shields.io/github.com/Infineon/makers-devops/actions/workflows/build.yml/badge.svg?branch=testpush)](https://github.com/Infineon/makers-devops/actions/workflows/build.yml)

[![Build Status](https://img.shields.io/github.com/Infineon/makers-devops/actions?style=plastic)](https://github.com/Infineon/makers-devops/actions)

[![Build Status](https://github.com/Infineon/makers-devops/workflows/CI/badge.svg)](https://github.com/Infineon/makers-devops/actions)
[![CI](https://img.shields.io/github.com/Infineon/makers-devops/actions/workflows/build.yml/badge.svg?branch=testpush)](https://github.com/Infineon/makers-devops/actions) -->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/Infineon/makers-devops">
    <img src="https://img.shields.io/badge/Arduino-white?style=plastic&logo=arduino&logoColor=00878F" alt="Logo" width="200">
  </a> -->

<h2 align="center">Makers-devops</h2>

  <p align="center">
    Makers' devops related template repository, i.e. workflows, special files, tool configs, ... .
    <br />
    <br />
    <a href="https://github.com/Infineon/makers-devops"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Infineon/makers-devops">View Demo</a>
    ·
    <a href="https://github.com/Infineon/makers-devops/issues/new?labels=bug&template=bug_report_template.md">Report Bug</a>
    ·
    <a href="https://github.com/Infineon/makers-devops/issues/new?labels=enhancement&template=feature_request_template.md">Request Feature</a>
   <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#How-to-run-Code-checks-locally">How to run Code checks locally</a>
      <ul>
        <li><a href="#Add-Repository-as-a-Submodule">Add Repository as a Submodule</a></li>
        <li><a href="#Configure-Your-Project">Configure Your Project</a></li>
        <li><a href="#Running-Locally">Running Locally</a></li>
          <ul>
            <li><a href="#To-execute-using-Docker-and-Make">To execute using Docker and Make</a></li>
            <li><a href="#To-execute-without-Docker">To execute without Docker</a></li>
          </ul>
        <li><a href="#Running-in-CI-CD">Running in CI CD</a></li>
        <li><a href="#Generating-Reports">Generating Reports</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This repository provides templates for creating a new project. The following files can be modified and reused:
1. README.md
2. SECURITY.md
3. CODE_OF_CONDUCT.md
4. CONTRIBUTING.md
5. LICENSE
6. templates/RELEASE_NOTES.md
7. .github/ISSUE_TEMPLATE/bug_report_template.md
8. .github/ISSUE_TEMPLATE/feature_request_template.md

It also provides a set of scripts and configurations to automate code quality checks and formatting for C/C++ and Python projects. It is designed to be integrated as a submodule in any project and includes workflows for running checks both locally and in GitHub Actions (GA) environments.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Features

1. Reusable Template Files
   
2. Scripts to Run Code Quality Checks:

   - cppcheck: Static analysis for C/C++ code.
   - clang-tidy: Linter and static analysis for C/C++ code.
   - clang-format: Code formatting for C/C++.
   - black: Code formatting for Python scripts.
  
3. Seamless Integration:

   - Can be added as a submodule to any project.
   - Supports local execution of code quality checks in development environments.
   - Includes a GitHub Actions workflow for CI/CD integration.

4. Customizable Checks:

    Project-specific and user-specific configurations using project.yml and user.yml.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<!-- * [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
*
* [![ThrowTheSwitch/Unity][Unity-logo]][Unity-url]
* [![Arduino][Arduino-logo]][Arduino-url]
* [![GCC][GCC-logo]][GCC-url]
* [![LLVM][LLVM-logo]][LLVM-url]
* [![MicroPython][MPY-logo]][MPY-url]
* [![ModusToolBox][MTB-logo]][MTB-url]
* [![Python][Python-logo]][Python-url] -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* <tool>
  ```sh
  <tool install >
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Infineon/makers-devops.git
   ```
2. Install dependencies
   ```sh
   <dependencies install>
   ```
3. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin Infineon/makers-devops
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How to run Code checks locally

### Add Repository as a Submodule

Include this repository as a submodule in your project using the following command:

```bash
git submodule add <repo_url> extras/makers-devops
```

### Configure Your Project

Create the following YAML files in your project to define the tools and checks to run:

- project.yml: Contains project-specific configurations such as tools and commands.
- user.yml: Optionally define user-specific configurations.

Add new tools and checks in the project.yml under the check: section to extend the configuration.

### Running Locally

#### To execute using Docker and Make

Ensure you have Docker installed to run containerized tools. The repository provides a Makefile to simplify execution of code quality checks. Some common commands include:

- Clean Results:
```sh
make clean-results
```

- Run All Checks:
```sh
make run-container-check-all
```

- Run Specific Tools:
```sh
make run-container-cppcheck
make run-container-clang-tidy-check
make run-container-clang-tidy-format
make run-container-black-format
```
For more details, refer to the Makefile in the repository.

#### To execute without Docker

Install the following tools locally:
- python3
- cppcheck
- llvm
- black
  
### Running in CI CD

The repository includes a predefined workflow script that can be triggered to run all the defined checks in the GitHub Actions (GA) environment. 

In order to integrate, reference the workflow script from this repository ".github/workflows/code_checks.yml".
Ensure your project sets the inputs, project-yaml and user-yaml for configuration.

### Generating Reports

After running cppcheck and clang-tidy, you can generate a collective HTML report:

```sh
make run-container-generate-html-report
```

The report will be available under the directory
_results/cppcheck/html-report/index.html

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://github.com/Infineon/makers-devops/blob/main/README.md)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/Infineon/makers-devops/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

We welcome community contributions! Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated** 👐.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Before submitting a pull request, please check the  [Code of Conduct](https://github.com/Infineon/makers-devops/blob/main/CODE_OF_CONDUCT.md) of this project. Thank you for following these guidelines.

Don't forget to give the project a star :star:! Thanks again!

### Important Note

Significant contributions should be aligned with the project team in advance.
See [CONTRIBUTING](CONTRIBUTING.md) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTORS -->
## Contributors

<a href="https://github.com/Infineon/makers-devops/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Infineon/makers-devops" alt="contrib.rocks image" width="50" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

<!-- Your Name - [](https://) - email@address -->

Project Link: [https://github.com/Infineon/makers-devops](https://github.com/Infineon/makers-devops)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

<!-- * [![ThrowTheSwitch/Unity][Unity-logo]][Unity-url]
* [![Arduino][Arduino-logo]][Arduino-url]
* [![GCC][GCC-logo]][GCC-url]
* [![LLVM][LLVM-logo]][LLVM-url] -->
<!-- * [![MicroPython][MPY-logo]][MPY-url]
* [![ModusToolBox][MTB-logo]][MTB-url]
* [![Python][Python-logo]][Python-url] -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[commit-shield]: https://img.shields.io/github/commit-activity/w/Infineon/makers-devops/main?style=plastic
[commit-url]: https://github.com/Infineon/makers-devops/commits
[commit2-shield]: https://img.shields.io/github/commit-activity/w/Infineon/makers-devops/main?style=plastic
[commit2-url]: https://github.com/Infineon/makers-devops/tree/main

[contributors-shield]: https://img.shields.io/github/contributors/Infineon/makers-devops.svg?style=plastic
[contributors-url]: https://github.com/Infineon/makers-devops/graphs/contributors

[contributor-covenant-shield]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
[contributor-covenant-url]: https://github.com/Infineon/makers-devops/blob/main/CODE_OF_CONDUCT.md

[doc-status-shield]: https://readthedocs.org/projects/xmc-arduino/badge/?version=latest
[doc-status-url]: https://xmc-arduino.readthedocs.io/en/latest/?badge=latest

[forks-shield]: https://img.shields.io/github/forks/Infineon/makers-devops.svg?style=plastic
[forks-url]: https://github.com/Infineon/makers-devops/network/members

[issues-shield]: https://img.shields.io/github/issues/Infineon/makers-devops.svg?style=plastic
[issues-url]: https://github.com/Infineon/makers-devops/issues

[license-shield]: https://img.shields.io/github/license/Infineon/makers-devops.svg?style=plastic
[license-url]: https://github.com/Infineon/makers-devops/blob/main/LICENSE

[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg?logo=pre-commit
[pre-commit-url]: https://github.com/pre-commit/pre-commit

[pull-request-shield]: https://img.shields.io/github/issues-pr-raw/Infineon/makers-devops.svg?style=plastic
[pull-request-url]: https://github.com/Infineon/makers-devops/pulls

[stars-shield]: https://img.shields.io/github/stars/Infineon/makers-devops.svg?style=plastic
[stars-url]: https://github.com/Infineon/makers-devops/stargazers

<!-- [product-screenshot]: images/screenshot.png -->


[Unity-logo]: https://img.shields.io/badge/ThrowTheSwitch_%2f_Unity-white?style=plastic
[Unity-url]: https://www.throwtheswitch.org/unity

[Arduino-logo]: https://img.shields.io/badge/Arduino-white?style=plastic&logo=arduino&logoColor=00878F
[Arduino-url]: https://www.arduino.org/

[GCC-logo]: https://img.shields.io/badge/GNU-white?style=plastic&logo=gnu&logoColor=A42E2B
[GCC-url]: https://www.gnu.org/

[LLVM-logo]: https://img.shields.io/badge/LLVM-white?style=plastic&logo=llvm&logoColor=262D3A
[LLVM-url]: https://www.llvm.org/

<!-- [MPY-logo]: https://img.shields.io/badge/MicroPython-white?style=plastic&logo=micropython&logoColor=262D3A
[MPY-url]: https://www.micropython.org/

[MTB-logo]: https://img.shields.io/badge/ModusToolBox-white?style=plastic
[MTB-url]: https://www.infineon.com/cms/en/design-support/tools/sdk/modustoolbox-software/

[Python-logo]: https://img.shields.io/badge/Python-white?style=plastic&logo=python&logoColor=3776AB
[Python-url]: https://www.python.org/ -->
