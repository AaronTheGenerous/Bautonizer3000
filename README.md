<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/6295/6295417.png" width="100" />
</p>
<p align="center">
    <h1 align="center">BAUTONIZER3000</h1>
</p>

<p align="center">
	<img src="https://img.shields.io/github/license/AaronTheGenerous/Bautonizer3000.git?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/AaronTheGenerous/Bautonizer3000.git?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/AaronTheGenerous/Bautonizer3000.git?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/AaronTheGenerous/Bautonizer3000.git?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/Selenium-43B02A.svg?style=flat&logo=Selenium&logoColor=white" alt="Selenium">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
</p>
<hr>

##  Quick Links

> - [ Overview](#-overview)
> - [ Features](#-features)
> - [ Repository Structure](#-repository-structure)
> - [ Modules](#-modules)
> - [ Getting Started](#-getting-started)
>   - [ Installation](#-installation)
>   - [ Running Bautonizer3000](#-running-Bautonizer3000)
>   - [ Tests](#-tests)
> - [ Project Roadmap](#-project-roadmap)
> - [ Contributing](#-contributing)
> - [ License](#-license)
> - [ Acknowledgments](#-acknowledgments)

---

##  Overview

Buttonizer3000 is a Python-based automation tool for managing promotional buttons on articles on a webpage. 
It allows users to schedule tasks for adding or removing promotional images and links to articles at specified times.


---

##  Features

Add promotional images and links to articles. Remove promotional images from articles. Schedule tasks to be executed at a future date and time. Task scheduling uses a secondary script to periodically check and execute pending tasks.

---

##  Repository Structure

```sh
└── Bautonizer3000/
    ├── .github
    │   └── workflows
    │       ├── code_quality.yml
    │       └── qodana_code_quality.yml
    ├── CODE_OF_CONDUCT.md
    ├── LICENSE.txt
    ├── NIK Buttons 10 CH.ico
    ├── README.md
    ├── __init__.py
    ├── bAUTOnizer3000.py
    ├── bAUTOnizer3000_stable.py
    ├── bAUTOnizer3000_temp.py
    ├── chromedriver.exe
    ├── exe_tasks.py
    ├── qodana.yaml
    ├── requirements.txt
    ├── temp.py
    └── test.py
```


---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version x.y.z`

###  Installation

1. Clone the Bautonizer3000 repository:

```sh
git clone https://github.com/AaronTheGenerous/Bautonizer3000.git
```

2. Change to the project directory:

```sh
cd Bautonizer3000
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

###  Running Bautonizer3000

Use the following command to run Bautonizer3000:

```sh
python main.py
```


---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/AaronTheGenerous/Bautonizer3000.git/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/AaronTheGenerous/Bautonizer3000.git/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/AaronTheGenerous/Bautonizer3000.git/issues)**: Submit bugs found or log feature requests for Bautonizer3000.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/AaronTheGenerous/Bautonizer3000.git
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is protected under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- Selenium 
- PyQt5

[**Return**](#-quick-links)

---
