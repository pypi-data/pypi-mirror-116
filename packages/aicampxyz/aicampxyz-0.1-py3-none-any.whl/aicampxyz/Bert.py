from colorama import Fore, Style


class Bert:
    def __init__(self):
        self.one_one = ""
        self.two_one = ""
        self.two_two = ""
        self.three_one = 0
        self.four_one = ""
        self.four_two = ""
        self.four_three = ""
        self.four_four = ""
        self.four_five = ""
        self.five_one = ""
        self.five_two = ""

    def test_question(self):
        print("What is the question's answer? (Answer: test)")
        question_input = input()
        if question_input == "test":
            print(Fore.GREEN + 'Correct')
        else:
            print(Fore.RED + 'Wrong')

    def first_question(self):
        print("What does it mean to \"pretrain deep bidirectional representations from unlabeled text?\"")
        question_input = input()
        self.one_one = question_input
        print(Fore.YELLOW + "Answer collected.")

    def second_question(self):
        print("What does it mean to \"fine-tune\" a model?")
        question_input = input()
        self.two_one = question_input
        print(Fore.YELLOW + "Answer collected.")
        print()
        print(Style.RESET_ALL)
        print("What is the point of pre-training in models like GPT and ELMo?")
        question_input = input()
        self.two_two = question_input
        print(Fore.YELLOW + "Answer collected.")

    def third_question(self):
        print("BERT advanced SOTA on how many \"sentence-level and token-level tasks\"?")
        question_input = input()
        self.three_one = question_input
        if question_input == '11':
            print(Fore.GREEN + "Correct")
        else:
            print(Fore.RED + "Wrong")

    def fourth_question(self):
        print("Category: What type of paper is this? A measurement paper? An analysis of an existing system? A description of a research prototype??")
        question_input = input()
        self.four_one = question_input
        print(Fore.YELLOW + "Answer collected.")
        print()
        print(Style.RESET_ALL)
        print("Context: Which other papers is it related to? Which theoretical bases were used to analyze the problem?")
        question_input = input()
        self.four_two = question_input
        print(Fore.YELLOW + "Answer collected.")
        print()
        print(Style.RESET_ALL)
        print("Correctness: Do the assumptions appear to be valid?")
        question_input = input()
        self.four_three = question_input
        print(Fore.YELLOW + "Answer collected.")
        print()
        print(Style.RESET_ALL)
        print("Contributions: What are the paper’s main contributions?")
        question_input = input()
        self.four_four = question_input
        print(Fore.YELLOW + "Answer collected.")
        print()
        print(Style.RESET_ALL)
        print("Clarity: Is the paper well written?")
        question_input = input()
        self.four_five = question_input
        print(Fore.YELLOW + "Answer collected.")

    def fifth_question(self):
        print("On what line in the code are the word probabilities drawn from the attention mechanism?")
        question_input = input()
        self.five_one = question_input
        print(Fore.YELLOW + "Answer collected.")
        print()
        print(Style.RESET_ALL)
        print("How do the \"query\" and \"key\" layers relate to (or result in) the word probabilities?")
        question_input = input()
        self.five_two = question_input
        print(Fore.YELLOW + "Answer collected.")

    def finish(self, path):
        file1 = open(path + "/results.txt", "a")
        file1.write(
            "What does it mean to \"pretrain deep bidirectional representations from unlabeled text\": " + self.one_one + "\n")
        file1.write(
            "What does it mean to \"fine-tune\" a model: " + self.two_one + "\n")
        file1.write(
            "What is the point of pre-training in models like GPT and ELMo: " + self.two_two + "\n")
        file1.write(
            "BERT advanced SOTA on how many \"sentence-level and token-level tasks\": " + self.three_one + "\n")
        file1.write("Category: What type of paper is this? A measurement paper? An analysis of an existing system? A description of a research prototype: " + self.four_one + "\n")
        file1.write(
            "Context: Which other papers is it related to? Which theoretical bases were used to analyze the problem: " + self.four_two + "\n")
        file1.write(
            "Correctness: Do the assumptions appear to be valid: " + self.four_three + "\n")
        file1.write(
            "Contributions: What are the paper’s main contributions: " + self.four_four + "\n")
        file1.write("Clarity: Is the paper well written: " +
                    self.four_five + "\n")
        file1.write("Clarity: Is the paper well written: " +
                    self.four_five + "\n")
        file1.write(
            "On what line in the code are the word probabilities drawn from the attention mechanism: " + self.five_one + "\n")
        file1.write(
            "How do the \"query\" and \"key\" layers relate to (or result in) the word probabilities: " + self.five_two + "\n")
        file1.close()
