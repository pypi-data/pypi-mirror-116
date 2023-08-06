from PyInquirer import style_from_dict, Token


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454 bold',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: 'bold',
})

""" StyleFirst = style_from_dict({
    "separator": '#cc5454',
    "questionmark": '#673ab7 bold',
    "selected": '#cc5454',  # default
    "pointer": '#673ab7 bold',
    "instruction": '',  # default
    "answer": '#f44336 bold',
    "question": '',
})

StyleSecond = style_from_dict({
    "separator": '#6C6C6C',
    "questionmark": '#FF9D00 bold',
    "selected": '#5F819D',
    "pointer": '#FF9D00 bold',
    "instruction": '',  # default
    "answer": '#5F819D bold',
    "question": '',
})


StyleThird = style_from_dict({
    "questionmark": '#E91E63 bold',
    "selected": '#673AB7 bold',
    "instruction": '',  # default
    "answer": '#2196f3 bold',
    "question": '',
})
 """
