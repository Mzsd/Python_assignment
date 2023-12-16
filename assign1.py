# Only used one library
import sys

### Helper Functions
#
#
# Helps to get detail which word currently the program is creating abbreviation from
# Used by abbreviate function only
def get_word_count(sub_words_length, i):
    for k, sl in enumerate(sub_words_length):
        if i < sl:
            word_counter = k
            break
    else:
        word_counter = k
    return word_counter

# This gives score to individual letter in the word
def give_score_to_letter(letter, counter, sub_words_length, sub_words, scores_val):
    # Get the current word count based on the lengths of sub_words
    word_counter = get_word_count(sub_words_length, counter)
    
    # Update the counter based on the length of the current sub_word
    counter = counter - sub_words_length[word_counter-1] if word_counter > 0 else counter
    
    # Get the length of the current sub_word
    word_length = len(sub_words[word_counter])
    
    score = 0
    # Check the different cases for assigning scores based on the position of the letter in the sub_word
    if counter == 0:
        pass  # Do nothing if the letter is at the first position
    elif counter == word_length - 1:
        # Assign score based on the position and letter (special case for 'E')
        if letter != 'E':
            score = 5
        else:
            score = 20
    elif counter == 1:
        # Assign score based on the position and letter using scores_val dictionary
        score = 1 + int(scores_val[letter])
    elif counter == 2:
        # Assign score based on the position and letter using scores_val dictionary
        score = 2 + int(scores_val[letter])
    elif counter > 2:
        # Assign score based on the position and letter using scores_val dictionary
        score = 3 + int(scores_val[letter])
    
    return score
#
#
### Helper Functions - END

# Main logic function which always keep 1st letter as 1st letter of abbreviation
# rest are created and score is calculated for each abbreviation.
def abbreviate(words, scores_val):
    abbrevs = list()
    
    # Split the input words into sub-words based on spaces and handle hyphens
    sub_words = words.replace("-", " ").split(' ')
    
    # Calculate the cumulative lengths of sub-words for position tracking
    sub_words_length = []
    length_sum = 0
    for k, w in enumerate(sub_words):
        length_sum += len(w) + 1 if k != len(sub_words) - 1 else len(w)
        sub_words_length.append(length_sum)    
        
    score = 0
    # Iterate over the positions in the input words to find potential abbreviations
    for i in range(1, len(words)):
        starting_letters = words[0]
        if words[i].isalpha():
            starting_letters += words[i]
            
            # Calculate score for the current position using the give_score_to_letter function
            score = give_score_to_letter(words[i].upper(), i, sub_words_length, sub_words, scores_val)
            
            abb = starting_letters
            new_score = score 
            # Iterate over subsequent positions to build potential abbreviations
            for j in range(i + 1, len(words)):
                if words[j].isalpha():
                    # Calculate score for the current position using the give_score_to_letter function
                    new_score += give_score_to_letter(words[j].upper(), j, sub_words_length, sub_words, scores_val)

                    abb += words[j]
                    if len(abb) > 2:                    
                        # Store potential abbreviation and its score
                        abbrevs.append((abb.upper(), new_score))
                        abb = starting_letters
                        new_score = score
    
    # Print the potential abbreviations and scores
    print("[+] Potential Abbreviations with Scores...", end='\n\n')    
    print(words + ':', abbrevs, end='\n\n')
    
    return abbrevs

# Based on the assignment logic to remove matching abbreviations in one or more phrases.
def reduce_abbrevs(abbrevs_list):
    # Create a set of possible abbreviations for each position
    poss_abbrevs = {k: {v[0] for v in abbrevs_list[k]} for k in abbrevs_list.keys()}
    
    # Flatten the sets of possible abbreviations into a single list
    flattened_ls = [v for k in poss_abbrevs.keys() for v in poss_abbrevs[k]]
    
    # Count the occurrences of each abbreviation in the flattened list
    count_dict = dict()
    for i in range(len(flattened_ls)):
        if flattened_ls[i] in count_dict:
            count_dict[flattened_ls[i]] += 1
        else:
            count_dict[flattened_ls[i]] = 1

    # Create a new dictionary to store reduced abbreviations
    new_poss_abbrevs = dict()
    for ck, ci in count_dict.items():
        # If the abbreviation occurs only once, add it to the new dictionary
        if ci == 1:
            for pk in poss_abbrevs.keys():
                for j in abbrevs_list[pk]:
                    if ck == j[0]:
                        new_poss_abbrevs.setdefault(pk, []).append(j)
    
    # Print the reduced abbreviations
    print("[+] Reduced Abbreviations...", end='\n\n')
    print(new_poss_abbrevs, end='\n\n')
    
    return new_poss_abbrevs

# Finalizes abbreviation and sort the abbreviations based on lowest score first.
def finalize_abbrev(poss_abbrevs):
    # Sort the potential abbreviations for each position based on their scores
    sorted_abbrevs = {key: sorted(value, key=lambda x: x[1]) for key, value in poss_abbrevs.items()}
    
    # Initialize dictionaries to store finalized abbreviations and their scores
    finalize_abbrevs_score = {}
    finalize_abbrevs = {}
    
    # Iterate over sorted abbreviations for each position
    for k, val in sorted_abbrevs.items():
        # Find the minimum score and corresponding abbreviations
        min_score = min(val, key=lambda x: x[-1])[-1]
        min_score_abbrev_score = [v for v in val if v[1] == min_score]
        min_score_abbrev = list({v[0] for v in val if v[1] == min_score})
        
        # Store the finalized abbreviations and their scores
        finalize_abbrevs_score[k] = min_score_abbrev_score
        finalize_abbrevs[k] = min_score_abbrev
        
    # Print the finalized abbreviations
    print("[+] Finalized Abbreviations...", end='\n\n')    
    print(finalize_abbrevs_score, end='\n\n')
    
    return finalize_abbrevs

# Generates and returns the output that was needed in the assignment
def return_output(poss_abbrevs_score: dict) -> str:
    # Generate a formatted string for the final output
    final_output = ''
    for k in poss_abbrevs_score.keys():
        final_output += k + '\n'
        for abb in poss_abbrevs_score[k]:
            final_output += abb + '\n'

    # Print the final output
    print("[+] Final Output...", end='\n\n')    
    print(final_output)
        
    return final_output

def main():
    input_filename = input("Enter the name of the input file: ")
    
    print("[+] Starting...")
    
    try:
        with open(input_filename) as fp:
            input_data = fp.read()
    except FileNotFoundError as e:
        print(f"{input_filename} not found!")
        sys.exit()
        
    print(f"[+] {input_filename} file fetched...")
    
    try:
        with open("values.txt") as fp:
            scores_data = fp.read()
    except FileNotFoundError as e:
        print("Scores file values.txt not found!")
        sys.exit()
        
    print("[+] scores file fetched...")    
    
    # Extract scores data and input words
    scores_val = {s.split(' ')[0]: s.split(' ')[-1] for s in scores_data.split('\n')}
    words = input_data.split('\n')
    
    print("[+] Generating abbreviations...")
    
    # Generate and process abbreviations for each word
    poss_abbrevs = reduce_abbrevs({w: abbreviate(w, scores_val) for w in words})
    
    # Finalize abbreviations and scores
    poss_abbrevs_score = finalize_abbrev(poss_abbrevs)
    
    # Generate the final formatted output
    final_output = return_output(poss_abbrevs_score)
    
    # Create an output file with a specific name
    output_filename = ''.join(['SIDDIQ_', input_filename.split('.')[0], '_abbrevs.', input_filename.split('.')[-1]])
    
    # Write the final output to the output file
    with open(output_filename, 'w') as fp:
        fp.write(final_output)
    
    print("[+] Program ended successfully.")    
    
        
if __name__ == '__main__':
    main()
