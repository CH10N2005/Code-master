questions_database = {
    "fill_in_blank": [
        {"question": "Python uses _____ for comments?", "answer": "#"},
        {"question": "To print in Python, we use the _____ function?", "answer": "print"},
        {"question": "HTML stands for HyperText _____ Language?", "answer": "Markup"},
        {"question": "CSS stands for Cascading Style _____?", "answer": "Sheets"},
        {"question": "JavaScript is an _____ programming language?", "answer": "interpreted"},
        {"question": "Variables in Python don't need _____ before use?", "answer": "declaration"},
        {"question": "Python uses _____ for indentation?", "answer": "spaces"},
        {"question": "To get user input in Python, we use the _____ function?", "answer": "input"},
        {"question": "Python lists are enclosed in square _____?", "answer": "brackets"},
        {"question": "To check the data type of a variable, we use the _____ function?", "answer": "type"},
        {"question": "Python strings can use single or double _____?", "answer": "quotes"},
        {"question": "To convert a value to an integer, we use the _____ function?", "answer": "int"},
        {"question": "Python functions are defined using the _____ keyword?", "answer": "def"},
        {"question": "To import modules in Python, we use the _____ keyword?", "answer": "import"},
        {"question": "Python dictionaries use _____ brackets?", "answer": "curly"},
        {"question": "The _____ loop in Python repeats while a condition is true?", "answer": "while"},
        {"question": "To create a list in Python, we use square _____?", "answer": "brackets"},
        {"question": "The _____ statement is used to exit a loop early?", "answer": "break"},
        {"question": "In HTML, links are created using the _____ tag?", "answer": "a"},
        {"question": "The _____ tag is used to create paragraphs in HTML?", "answer": "p"},
        {"question": "In CSS, the color property changes the _____ color?", "answer": "text"},
        {"question": "Python uses _____ to represent true and false values?", "answer": "bool"},
        {"question": "The _____ function returns the length of a list?", "answer": "len"},
        {"question": "To add an item to a list, we use the _____ method?", "answer": "append"},
        {"question": "The _____ operator is used for exponentiation in Python?", "answer": "**"},
        {"question": "HTML images are inserted using the _____ tag?", "answer": "img"},
        {"question": "The _____ attribute specifies the URL of a link in HTML?", "answer": "href"},
        {"question": "In Python, _____ is used to define a class?", "answer": "class"},
        {"question": "The _____ keyword is used to handle exceptions in Python?", "answer": "try"},
        {"question": "CSS uses _____ to select elements by their class name?", "answer": "dot"}
    ],
    "true_false": [
        {"question": "HTML is a programming language?", "answer": False},
        {"question": "Python is case-sensitive?", "answer": True},
        {"question": "CSS is used for website styling?", "answer": True},
        {"question": "JavaScript and Java are the same language?", "answer": False},
        {"question": "Python uses semicolons to end statements?", "answer": False},
        {"question": "Variables in Python can start with numbers?", "answer": False},
        {"question": "Python supports multiple inheritance?", "answer": True},
        {"question": "HTML tags are case-sensitive?", "answer": False},
        {"question": "CSS can be written inside an HTML file?", "answer": True},
        {"question": "Python is an interpreted language?", "answer": True},
        {"question": "All HTML tags must be closed?", "answer": False},
        {"question": "Python lists can contain different data types?", "answer": True},
        {"question": "JavaScript runs only in browsers?", "answer": False},
        {"question": "Python was created by Guido van Rossum?", "answer": True},
        {"question": "HTML5 is the latest version of HTML?", "answer": True},
        {"question": "Python indentation is optional?", "answer": False},
        {"question": "The <div> tag is a block-level element in HTML?", "answer": True},
        {"question": "CSS stands for Computer Style Sheets?", "answer": False},
        {"question": "Python lists are immutable?", "answer": False},
        {"question": "The <head> tag contains the visible content of a webpage?", "answer": False},
        {"question": "JavaScript can be used for both front-end and back-end development?", "answer": True},
        {"question": "In Python, strings are mutable?", "answer": False},
        {"question": "The <br> tag in HTML requires a closing tag?", "answer": False},
        {"question": "Python supports object-oriented programming?", "answer": True},
        {"question": "CSS can only be written in external files?", "answer": False},
        {"question": "The == operator in Python checks for equality?", "answer": True},
        {"question": "HTML stands for Hyper Transfer Markup Language?", "answer": False},
        {"question": "Python was first released in 1991?", "answer": True},
        {"question": "The <title> tag appears in the browser tab?", "answer": True},
        {"question": "In Python, 0 is considered as False?", "answer": True}
    ]
}

# Function to get a shuffled list of all questions
def get_shuffled_questions():
    import random
    
    all_questions = (
        questions_database["fill_in_blank"] + 
        questions_database["true_false"]
    )
    
   
    random.shuffle(all_questions)
    
    return all_questions

# Separate lists for different question types
fillinblankquestions = [(q["question"], q["answer"]) for q in questions_database["fill_in_blank"]]
TFquestions = [(q["question"], q["answer"]) for q in questions_database["true_false"]]