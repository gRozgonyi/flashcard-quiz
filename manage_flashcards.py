import os
import pickle

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class FlashcardCollection:
    def __init__(self, name):
        self.name = name
        self.flashcards = {}
        self.load_from_file()  # Load flashcards from file upon collection creation

    def add_flashcard(self, question, answer):
        self.flashcards[question] = answer
        self.save_to_file()  # Save flashcards to file after adding a flashcard

    def remove_flashcard(self, question):
        if question in self.flashcards:
            del self.flashcards[question]
            self.save_to_file()  # Save flashcards to file after removing a flashcard

    def save_to_file(self):
        folder_path = "collections"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        file_path = os.path.join(folder_path, f"{self.name}.pkl")
        with open(file_path, "wb") as file:
            pickle.dump(self.flashcards, file)

    def load_from_file(self):
        folder_path = "collections"
        file_path = os.path.join(folder_path, f"{self.name}.pkl")

        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                self.flashcards = pickle.load(file)

def prompt_for_flashcards(collection):
    while True:
        question = input("   Enter the question: ")
        if question.lower() == 'exit':
            return

        answer = input("   Enter the answer: ")

        collection.add_flashcard(question, answer)
        print(f"   Flashcard added: {question} - {answer}")

def prompt_for_flashcard_removal(collection):
    while True:
        
        if not collection.flashcards:
            print("No flashcards left in the collection.")
            break

        question = input("   Enter the question to remove: ")
        if question.lower() == 'exit':
            break

        answer = collection.flashcards.get(question)

        collection.remove_flashcard(question)
        print(f"   Flashcard removed: {question} - {answer}")

def create_new_collection():
    name = input("Enter the name for the new collection: ")
    collection = FlashcardCollection(name)
    print(f"\n Collection '{name}' has been created.")
    print(" Enter flashcards. Type 'exit' for the question to finish.")
    prompt_for_flashcards(collection)

def list_existing_collections():
    folder_path = "collections"
    if not os.path.exists(folder_path):
        return []
    
    existing_collections = [filename[:-4] for filename in os.listdir(folder_path) if filename.endswith(".pkl")]
    return existing_collections

def delete_collection(collection_name):
    folder_path = "collections"
    file_path = os.path.join(folder_path, f"{collection_name}.pkl")

    if os.path.exists(file_path):
        confirm = input(f"\n Are you sure you want to delete '{collection_name}'? (y): ")
        if confirm.lower() == 'y':
            os.remove(file_path)
            print(f" Collection '{collection_name}' has been deleted.")
    else:
        print(f"\n Collection '{collection_name}' does not exist.")

def edit_existing_collection():

    existing_collections = list_existing_collections()

    if not existing_collections:
        print(" No existing collections found.")
        return

    print(" Existing collections:")
    for idx, collection_name in enumerate(existing_collections, 1):
        print(f" {idx}. {collection_name}")
    
    while True:
        choice = input("Enter the number of the collection to edit (or type 'exit' to cancel): ")
        if choice.lower() == 'exit':
            return

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(existing_collections):
                selected_collection = existing_collections[choice_idx]
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a valid number.")

    collection = FlashcardCollection(selected_collection)
    print(f" Collection '{selected_collection}' has been loaded.")

    while True:
        print("\n Menu:")
        print(" 1. Add flashcards")
        print(" 2. Remove flashcards")
        print(" 3. Print flashcards")
        print(" 4. Delete collection")
        print(" 5. Return to main menu")

        choice = input(" Enter your choice (1, 2, 3, 4 or 5): ")

        if choice == '1':
            print("  Enter flashcards. Type 'exit' for the question to finish.")
            prompt_for_flashcards(collection)
        elif choice == '2':
            print("  Remove flashcards. Type 'exit' to finish.")
            prompt_for_flashcard_removal(collection)
        elif choice == '3':
            print("  Flashcards in the collection:")
            for idx, (question, answer) in enumerate(collection.flashcards.items(), 1):
                print(f"  {idx}. {question}")
                print(f"     {answer}")
        elif choice == '4':
            delete_collection(selected_collection)
        elif choice == '5':
            collection.save_to_file()  # Save the collection before returning to the main menu
            print(f"\n  Collection '{selected_collection}' has been updated.")
            break  # Exit the edit mode and return to the main menu
        else:
            print(" Invalid choice. Please enter 1, 2, 3, or 4.")

def main():
    print("Welcome to Manage My Flashcards!")
    while True:
        print("\nMenu:")
        print("1. Create new collection")
        print("2. Edit existing collection")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            create_new_collection()
        elif choice == '2':
            edit_existing_collection()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()