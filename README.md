# Project Overview

Welcome to the **ai-readme-generator** repository! This project aims to simplify the process of creating README files for your GitHub projects using AI. By leveraging advanced algorithms, the ai-readme-generator can generate comprehensive and structured README files that enhance the presentation of your projects.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [GitHub Fetching Process](#github-fetching-process)
- [License](#license)

## Installation

To get started with the ai-readme-generator, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/leopoldsprenger/ai-readme-generator.git
   ```
2. Navigate into the project directory:
   ```bash
   cd ai-readme-generator
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To generate a README file, simply run the main script:

```bash
python main.py
```

This command will initiate the application, and a chat window will pop up, guiding you through the process of generating your README file.

**Warning:** Please note that the AI might take some time to generate responses, depending on the complexity of the input data.

## GitHub Fetching Process

The ai-readme-generator can fetch data from GitHub to enhance the README generation process. This is done using the `PyGithub` library to interact with the GitHub API. The following code snippet demonstrates how to retrieve all text files from a specified repository:

```python
from github import Github

def get_all_text_files(repo):
    """
    Retrieves all text files in the repository.
    Returns a dictionary with file paths as keys and file contents as values.
    """
    print(f"Getting all files from repository: {repo.full_name}")

    files_dict = {}
    binary_files = []
    contents = repo.get_contents("")  # Start from the root directory

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":  # If it's a directory, fetch its contents
            contents.extend(repo.get_contents(file_content.path))
        else:  # If it's a file, check if it's a text file
            try:
                # Attempt to decode content to filter out binary files
                content = file_content.decoded_content.decode("utf-8")
                files_dict[file_content.path] = content
            except UnicodeDecodeError:
                # Skip binary files that cannot be decoded
                binary_files.append(file_content.path)

    return files_dict, binary_files

def get_files_from_repo(username, repo_name, pat_token):
    """Fetches all text files from a GitHub repository."""
    github = Github(pat_token)
    repository = github.get_repo(f"{username}/{repo_name}")
    return get_all_text_files(repository)
```

This function retrieves all text files from the specified GitHub repository, returning their file paths and contents while filtering out binary files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
