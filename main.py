import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import chatbot
import scrape_github_repo
import os

class ReadmeGeneratorThread(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)

    def __init__(self, username, repo_name, pat_token):
        super().__init__()
        self.username = username
        self.repo_name = repo_name
        self.pat_token = pat_token

    def run(self):
        self.update_signal.emit("Fetching files from repository...")
        files_dict, binary_files = scrape_github_repo.get_files_from_repo(self.username, self.repo_name, self.pat_token)

        self.update_signal.emit("Creating summaries for each file...")
        summarized_files = {}
        for file_name, file_content in files_dict.items():
            summarized_files[file_name] = chatbot.get_response(chatbot.prompts["one file summary"] + "\nFiles: " + str(file_content))

        self.update_signal.emit("Synthesizing into one README file...")
        readme_content = chatbot.get_response(chatbot.prompts["generate readme"] + f"\nThe repository is named {self.repo_name} and my username is {self.username}" + "\nFile summaries: " + str(summarized_files) + "\nBinary Files: " + str(binary_files))

        self.update_signal.emit("Saving README file...")
        with open("content/README.md", "w") as file:
            file.write(readme_content)

        self.finished_signal.emit("README generation complete. You can now request modifications.")

class ChatGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.readme_content = ""
        self.username = ""
        self.repo_name = ""
        self.pat_token = ""
        self.step = 0  # Step tracking for input
        self.chat_display.append("Bot: Please input your GitHub username.")

    def initUI(self):
        self.setWindowTitle("GitHub README Generator")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter username...")
        self.input_field.returnPressed.connect(self.handle_input)
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_input)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    def handle_input(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        self.chat_display.append(f"You: {user_input}")
        self.input_field.clear()

        if self.step == 0:
            self.username = user_input
            self.input_field.setPlaceholderText("Enter repository name...")
            self.chat_display.append("Bot: Please enter the repository name.")
        elif self.step == 1:
            self.repo_name = user_input
            self.input_field.setPlaceholderText("Enter PAT token...")
            self.chat_display.append("Bot: Please enter your PAT token.")
        elif self.step == 2:
            self.pat_token = user_input
            self.input_field.setEnabled(False)
            self.send_button.setEnabled(False)
            self.chat_display.append("Bot: Generating README file, please wait...")

            self.readme_thread = ReadmeGeneratorThread(self.username, self.repo_name, self.pat_token)
            self.readme_thread.update_signal.connect(self.update_chat)
            self.readme_thread.finished_signal.connect(self.enable_chat)
            self.readme_thread.start()
        else:
            self.modify_readme(user_input)

        self.step += 1

    def update_chat(self, message):
        self.chat_display.append(f"Bot: {message}")

    def enable_chat(self, message):
        self.chat_display.append(f"Bot: {message}")
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setPlaceholderText("Request modifications...")

    def modify_readme(self, user_input):
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.chat_display.append("Bot: Making changes...")

        self.readme_content = chatbot.get_response(chatbot.prompts["generate readme"] + f"\nThe repository is named {self.repo_name} and my username is {self.username}" + "\nReadme file: " + self.readme_content + "\nUser input: " + user_input)

        os.rename("content/README.md", "content/README-backup.md")
        with open("content/README.md", "w") as file:
            file.write(self.readme_content)

        confirmation_response = chatbot.get_response(chatbot.prompts["answer user"] + f"\nUser: {user_input}")
        self.chat_display.append(f"Bot: {confirmation_response}")
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGUI()
    window.show()
    sys.exit(app.exec_())
