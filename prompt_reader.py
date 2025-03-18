def read_prompt(file_path='prompt.txt'):
    try:
        with open(file_path, 'r') as file:
            prompt = file.read()
        return prompt
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file {file_path}: {e}")
        return None

if __name__ == "__main__":
    prompt = read_prompt()
    if prompt:
        print("Prompt content:")
        print(prompt)