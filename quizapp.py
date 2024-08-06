def ask_question(question,answer):
    """Asks questions and checks user's input/answer """
    user_answer = input(question)
    if user_answer.lower()==answer.lower():
        print("Correct!")
        return True        
    else:
        print("Incorrect!")
        return False
    
def main():
    print("Welcome to the quiz game of Python!")
    
    points=0
    questions= [ 
        ("5+9","14"),
        ("1*9","9"),
        ("4/5 in decimal","0.8"),
        ("Capital of Nigeria","Abuja"),
        ("F_st","a"or"i"),
        ("Mean of 5,5,6,7,9 is","6.4")
    ]
    
    for question, answer in questions:
        if ask_question(question, answer):
            points+=1
        
    print(f"You scored {points} out of {len(questions)}")
    if points==len(questions):
        print("Perfect Score!")
    else:
        print('Not perfect!')
        
if __file__ == "__main__":
    main()