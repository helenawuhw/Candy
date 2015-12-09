class LUTindex:
    def __init__(self):
        self.hashmap = dict()
        self.add_elements()
        self.key_elements = self.all_key_elements()

    def add_elements(self):
        self.hashmap.setdefault(' ', 'Okay')
        self.hashmap.setdefault('I am hungry', 'Let\'s get food')
        self.hashmap.setdefault('I am sleepy', 'You should go to bed')
        self.hashmap.setdefault('I am not hungry', 'Then starve')
        self.hashmap.setdefault('I am okay', 'Thats good')
        self.hashmap.setdefault('I am doing well', 'Thats good')
        self.hashmap.setdefault('It is raining outside', 'Get an umbrella')
        self.hashmap.setdefault('It is sunny outside', 'Enjoy the sunshine')
        self.hashmap.setdefault('Bear you are dumb', 'Not as stupid as you')
        self.hashmap.setdefault('What is the time right now', 'No clue check your watch')
        self.hashmap.setdefault('Are you alive', 'Of course I am')
        self.hashmap.setdefault('Hello', 'Hello')
        self.hashmap.setdefault('Hi', 'Hi')
        self.hashmap.setdefault('How is it going', 'It is going well')
        self.hashmap.setdefault('Are you human', 'Of course I am')
        self.hashmap.setdefault('Prove that you are human', 'I do not need to')
        self.hashmap.setdefault('I am not going to be on time', 'It is okay to be late once in a while')
    def all_key_elements(self):
        theview = self.hashmap.viewkeys()
        iterview = iter(theview)
        list = []
        for element in iterview:
            list.append(element)
        return list

    def get_key_elements(self):
        return self.key_elements

    def get_response(self, key):
        return self.hashmap.get(key)