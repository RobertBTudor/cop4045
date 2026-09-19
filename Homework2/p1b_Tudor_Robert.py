
def parse_functions(filename: str) -> tuple:
    """
    Parses a Python file and returns information about its functions.
    Each function is returned as a tuple containing its line number,
    name, argument list, and function code. Empty lines and
    comments are removed from the function code.
    """

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        # Creates an empty list where we will store information about each function in the file
        functions = []
        i = 0

        # Continues examining lines until i reaches the end of the file.
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("def "):
                # Stores the actual line number of the function definition.
                line_number = i + 1

                #Removes comments from the function as well as whitespace
                definition = line.split("#")[0].strip()

                # Finds the name of the function by searching between "def " and "(" 
                start = definition.index("def ") + 4
                end = definition.index("(")
                function_name = definition[start:end]

                # Extracts everything between the parentheses, giving the argument list as a string.
                args_start = definition.index("(") + 1
                args_end = definition.rindex(")")
                arguments = definition[args_start:args_end]

                function_code = [definition + "\n"]
                i += 1

                # Continues reading lines until we reach the end of the file, or reach next function def
                while i < len(lines):
                    current_line = lines[i]

                    if not current_line.startswith((" ", "\t")):
                        break

                    # Removes any comment while keeping the original indentation
                    code_line = current_line.split("#")[0].rstrip()

                    if code_line:
                        function_code.append(code_line + "\n")
                    i += 1

                # Adds the function's line number, name, arguments, and code to the functions list
                functions.append((
                    line_number,
                    function_name,
                    arguments,
                    "".join(function_code)
                ))
            else:
                i += 1

        # Sorts the functions alphabetically using element 1 of each tuple (function name)
        functions.sort(key=lambda function: function[1])
        #Return the list as a tuple
        return tuple(functions)
    
    # Catches any error that occurs while opening, reading, or parsing
    except Exception as error:
        print(f"Error parsing file '{filename}': {error}")
        raise


def main(): 
    result = parse_functions("funs.py") 
    print(result) 

if __name__ == "__main__": 
    main()