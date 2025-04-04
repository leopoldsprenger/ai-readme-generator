from g4f.client import Client

def get_response(content, model="gpt-4o-mini"):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        web_search=False
    )
    return response.choices[0].message.content

prompts = {
    "one file summary": "Please summarize this file briefly in markdown and don't add any text other than the summary to your answer. Include a 2 sentence summary of the code function and any explanation for sections that could be important to mention in a readme file for any repository that file may be in: ",
    "generate readme": "Take all of these readme files and generate a single readme file for the entire repository. Don't write the markdown decleration symbols before and after the contents of the readme file, just return it's contents. Also don't add anything like 'here is the contents of the readme file', just return the readme file without any further explanation. Make it interactive with distinct sections like installation, usage, and license. Include installation instructions, usage examples, and license information. Also make a project overview section that includes a brief description of the project and its purpose with links to clickable headers. Please also use the names of the provided binary files and include them as embeds in the readme file when you think applicable (use the file names and endings as contest clues). If you find an already existing readme in the files I list, please restructure it or completely rewrite it depending on how in-depth it is, since the user wants a new one.",
    "answer user": "You have changed the readme.md file to the users request. Please write a short chat-like confirmation message such that you have done the thing x they asked you to do. Don't say anything else. Example: 'Thank you for your request! I have generated a new readme file for the repository with changes: user_changes here'"
}

if __name__ == '__main__':
    print(get_response("This is a test to see if you work correctly..."))
