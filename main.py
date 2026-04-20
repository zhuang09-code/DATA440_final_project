from src.data_gen import generate_data
from src.user_input import get_user_query

def main():
    print("Hello from data440-final-project!")
    query = get_user_query()
    data = generate_data(query)
    return print(data)

if __name__ == "__main__":
    main()
