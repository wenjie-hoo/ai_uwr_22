def read_words(filename):
    with open(filename, encoding='utf-8') as f:
        return {word.strip() for word in f}

def split_text(text, words, memo):
    if text in memo:
        return memo[text]

    best_division = ''
    best_score = 0

    for i in range(1, len(text) + 1):
        prefix = text[:i]
        if prefix in words:
            suffix_division, suffix_score = split_text(text[i:], words, memo)
            current_score = len(prefix) ** 2 + suffix_score
            if current_score > best_score:
                best_division = prefix + ' ' + suffix_division
                best_score = current_score

    memo[text] = (best_division, best_score)
    return memo[text]

def main(input_file, output_file, words_file):
    words = read_words(words_file)
    with open(input_file, encoding='utf-8') as input_f, open(output_file, 'w', encoding='utf-8') as output_f:
        for line in input_f:
            line = line.strip()
            splited_text = split_text(line, words, {})
            output_f.write(f'{splited_text[0]}\n')

if __name__ == '__main__':
    main('./zad2_input.txt','./zad_output.txt', './words_for_ai1.txt')