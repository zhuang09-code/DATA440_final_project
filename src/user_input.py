def get_user_query() -> str:
    """
    Ask the user to enter research interests and return the input
    """

    while True:
        user_input = input("Enter your research interests: ")
        user_input = user_input.strip()

        if user_input != "":
            return user_input
        
        print("No valid input was entered. Please enter at least one research interest.")
    
    return None