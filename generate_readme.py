import chatbot
import scrape_github_repo
import os

def chat_for_improvements(readme_content, summarized_files, binary_files, send_message_callback):
    """Allows users to request modifications to the README through the GUI."""
    send_message_callback("You can now chat with the AI to suggest improvements.")

    def process_chat(user_query):
        """Handles user input and updates the README."""
        if user_query.lower() == "exit":
            return None  # GUI will handle exit logic

        updated_readme = chatbot.get_response(
            chatbot.prompts["generate readme"] +
            f"\nFile summaries: {str(summarized_files)}\nBinary Files: {str(binary_files)}\nUser input: {user_query}"
        )

        # Save backup and write new README
        os.rename("content/README.md", "content/README-backup.md")
        with open("content/README.md", "w") as file:
            file.write(updated_readme)

        confirmation_response = chatbot.get_response(chatbot.prompts["answer user"] + f"\nUser: {user_query}")
        return confirmation_response

    return process_chat  # Return function for GUI to handle chat interactions

def generate_readme(username, repo_name, pat_token, send_message_callback):
    """Generates the README file and updates the GUI with progress messages."""

    send_message_callback("Fetching files from GitHub...")
    files_dict, binary_files = scrape_github_repo.get_files_from_repo(username, repo_name, pat_token)

    send_message_callback("Creating summaries for each file...")
    summarized_files = {}
    for file_name, file_content in files_dict.items():
        summarized_files[file_name] = chatbot.get_response(chatbot.prompts["one file summary"] + file_content)

    send_message_callback("Synthesizing into one README file...")
    readme_content = chatbot.get_response(
        chatbot.prompts["generate readme"] +
        f"\nFile summaries: {str(summarized_files)}\nBinary Files: {str(binary_files)}"
    )

    send_message_callback("Saving README file...")
    os.makedirs("content", exist_ok=True)
    with open("content/README.md", "w") as file:
        file.write(readme_content)

    send_message_callback("README file created successfully!")

    return chat_for_improvements(readme_content, summarized_files, binary_files, send_message_callback)
