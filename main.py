from src.data_gen import generate_data
from src.user_input import get_user_query
from src.output import display_top_professors

def main():
    print("Hello from data440-final-project!")
    query = get_user_query()
    data = generate_data(query)
    output = display_top_professors(data)
    return output

if __name__ == "__main__":
    main()
