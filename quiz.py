import requests
from random import shuffle

class Quiz:

    def connect(self, category):
        url = "https://opentdb.com/api.php?amount=10&category={}&type=multiple".format(category)
        timeout = 5
        try:
            # requesting URL
            # request = requests.get(url)
            data = requests.get(url, timeout=timeout)
            test_data = data.json()
            # extract questions, options and answers
            self.all_questions = []
            self.all_options = []
            self.all_correct = []
            for result in test_data['results']:
                self.all_questions.append(result['question'])
                self.all_correct.append(result['correct_answer'])
                options = []
                options.append(result['correct_answer'])
                options.extend(result['incorrect_answers'])
                shuffle(options)
                self.all_options.append(options)
            return 1
        # if the url don't response
        except (requests.ConnectionError, requests.Timeout) as exception:
            return 0

    # returns questions
    def extract_questions(self):
        return self.all_questions

    # returns all options
    def extract_options(self):
        return self.all_options

    # returns correct answers
    def extract_answers(self):
        return self.all_correct
