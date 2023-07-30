import random
from manage_flashcards import FlashcardCollection, list_existing_collections

def welcome_quizzer():
    print("Welcome to the Quizzer!")
    print("Available collections:")
    existing_collections = list_existing_collections()
    for idx, collection_name in enumerate(existing_collections, 1):
        print(f"{idx}. {collection_name}")

    return existing_collections

def get_quiz_collection():
    existing_collections = welcome_quizzer()
    while True:
        choice = input("Enter the number of the collection to be tested on (or type 'exit' to quit): ")
        if choice.lower() == 'exit':
            return None

        try:
            choice_idx = int(choice) - 1
            selected_collection = existing_collections[choice_idx]
            return selected_collection
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")

def quiz():
    selected_collection = get_quiz_collection()

    if not selected_collection:
        print("Quizzing canceled.")
        return

    collection = FlashcardCollection(selected_collection)
    flashcards = list(collection.flashcards.items())
    total_flashcards = len(flashcards)
    correct_answers = 0
    total_attempts = 0

    print(f"\nQuiz started for collection '{selected_collection}'.")
    while flashcards:
        question, answer = random.choice(flashcards)
        user_answer = input(f"Question: {question}\nYour Answer: ")
        total_attempts += 1

        if user_answer.lower() == 'exit':
            break
        elif user_answer.lower() == answer.lower():
            correct_answers += 1
            print(f"Correct! {correct_answers}/{total_flashcards}")
            flashcards.remove((question, answer))
        else:
            print(f"Incorrect. The correct answer is: {answer}. {correct_answers}/{total_flashcards}")

    print("Quiz finished!")
    print(f"You answered {correct_answers} out of {total_flashcards} flashcards correctly.")
    print(f"Total attempts: {total_attempts}")

if __name__ == "__main__":
    quiz()