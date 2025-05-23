import random

LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SPECIAL = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~"

def word_in_file(word, filename, case_sensitive=False):
    """Checks if the word exists in a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if (case_sensitive and word == line.strip()) or (not case_sensitive and word.lower() == line.strip().lower()):
                    return True
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return False

def word_has_character(word, character_list):
    """Checks if the word contains at least one character from the specified list."""
    return any(char in character_list for char in word)

def word_complexity(word):
    """Calculates password complexity based on the types of characters used."""
    complexity = 0
    complexity += word_has_character(word, LOWER)
    complexity += word_has_character(word, UPPER)
    complexity += word_has_character(word, DIGITS)
    complexity += word_has_character(word, SPECIAL)
    return complexity

def suggest_improvements(password):
    """Suggests improvements to make the password stronger."""
    suggestions = []
    if not word_has_character(password, UPPER):
        suggestions.append("Add uppercase letters.")
    if not word_has_character(password, DIGITS):
        suggestions.append("Include numbers.")
    if not word_has_character(password, SPECIAL):
        suggestions.append("Use special symbols.")
    if len(password) < 15:
        suggestions.append("Increase password length.")
    
    return suggestions if suggestions else ["Your password is strong!"]

def generate_secure_password(length=16):
    """Generates a strong random password."""
    all_chars = LOWER + UPPER + DIGITS + SPECIAL
    return ''.join(random.choice(all_chars) for _ in range(length))

def password_strength(password, min_length=10, strong_length=15):
    """Evaluates password strength and prints the appropriate message."""
    if word_in_file(password, 'wordlist.txt'):
        print("The password is a dictionary word and is not secure.")
        return 0
    if word_in_file(password, 'toppasswords.txt', case_sensitive=True):
        print("The password is a commonly used password and is not secure.")
        return 0
    if len(password) < min_length:
        print("The password is too short and is not secure.")
        return 1
    if len(password) > strong_length:
        print("The password is long, the length exceeds complexity, this is a good password.")
        return 5
    
    score = 1 + word_complexity(password)
    improvements = suggest_improvements(password)
    print(f"Suggestions to improve password: {', '.join(improvements)}")
    
    return score

def main():
    """User input loop for password testing."""
    while True:
        print("\nOptions:")
        print("1. Test a password")
        print("2. Generate a secure password")
        print("3. Quit")
        choice = input("Select an option (1/2/3): ")

        if choice == '1':
            password = input("Type a password to test: ")
            score = password_strength(password)
            print(f"Password score: {score}")
        elif choice == '2':
            secure_password = generate_secure_password()
            print(f"Generated secure password: {secure_password}")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == '__main__':
    main()