def line_number(input_file, output_file):
    """
    Function:
        Copies a text file and add line numbers
        Reads the input_file and then outputs the file into output_file with the lines numbered.
        
    Parameters:
        input_file: name of the text file to read.
        output_file: name of the text file to write.
    Returns:
        None
    """
    try:
        infile = open(input_file, "r")
        outfile = open(output_file, "w")

        count = 1
        for line in infile:
            outfile.write(str(count) + ": " + line)
            count = count + 1

        infile.close()
        outfile.close()

    except Exception:
        print("Sorry, something went wrong with the files.")
        raise

def main():
    # Define the input and output file
    input_filename = "p1_Tudor_Robert_INPUT.txt"
    output_filename = "p1_Tudor_Robert_OUTPUT.txt"

    # Make sure the file names are not the same
    if input_filename == output_filename:
        print("Error: You cannot use the same name for both files")
    else:
        #Call the function 
        line_number(input_filename, output_filename)
        print("Success! A numbered copy has been created in: ", output_filename)


# Run the main function
if __name__ == "__main__":
    main()