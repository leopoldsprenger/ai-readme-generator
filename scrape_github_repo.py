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
