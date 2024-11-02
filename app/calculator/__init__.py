import os
import logging
import logging.config
from dotenv import load_dotenv
from app.operations import addition, subtraction, multiplication, division
from app.history import History

# Initialize logging and environment variables
def initialize_logging():
    logging_conf_path = 'logging.conf'
    if os.path.exists(logging_conf_path):
        logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging configured.")

def load_env_variables():
    load_dotenv()
    environment = os.getenv("ENVIRONMENT", "PRODUCTION")
    logging.info(f"Environment loaded: {environment}")
    return environment

def calculator():
    """Basic REPL calculator that performs addition, subtraction, multiplication, and division, with history and logging support."""
    
    # Initialize history and logging
    history = History()
    initialize_logging()
    load_env_variables()
    
    # Print a welcome message and instructions.
    print("Welcome to the calculator REPL! Type 'exit' to quit.")
    print("You can also type 'history' to view past calculations, 'clear' to clear history, or 'undo' to remove the last calculation.")

    # Start the REPL loop.
    while True:
        # Prompt the user for input.
        user_input = input("Enter an operation (add, subtract, multiply, divide) and two numbers, or a command: ")

        # Handle the 'exit' command.
        if user_input.lower() == "exit":
            logging.info("User exited the calculator.")
            print("Exiting calculator...")
            break

        # Handle the 'history' command.
        elif user_input.lower() == "history":
            logging.info("User requested calculation history.")
            print("Calculation History:")
            for calc in history.get_history():
                print(calc)
            continue

        # Handle the 'clear' command.
        elif user_input.lower() == "clear":
            history.clear_history()
            logging.info("User cleared the calculation history.")
            print("History cleared.")
            continue

        # Handle the 'undo' command.
        elif user_input.lower() == "undo":
            history.undo_last()
            logging.info("User undid the last calculation.")
            print("Last calculation undone.")
            continue

        # Process the input as a calculation.
        else:
            try:
                operation, num1, num2 = user_input.split()
                num1, num2 = float(num1), float(num2)
            except ValueError:
                logging.error("Invalid input format provided by user.")
                print("Invalid input. Please follow the format: <operation> <num1> <num2>")
                continue

            # Perform the requested operation.
            try:
                if operation == "add":
                    result = addition(num1, num2)
                elif operation == "subtract":
                    result = subtraction(num1, num2)
                elif operation == "multiply":
                    result = multiplication(num1, num2)
                elif operation == "divide":
                    result = division(num1, num2)
                else:
                    logging.warning(f"Unknown operation '{operation}' provided by user.")
                    print(f"Unknown operation '{operation}'. Supported operations: add, subtract, multiply, divide.")
                    continue
                
                # Log and store the calculation
                calculation_str = f"{operation} {num1} {num2} = {result}"
                history.add_calculation(calculation_str)
                logging.info(f"Performed calculation: {calculation_str}")

                # Print the result.
                print(f"Result: {result}")

            except ValueError as e:
                logging.error(f"Error during division: {e}")
                print(e)
