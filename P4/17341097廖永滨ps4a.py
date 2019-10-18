# Problem Set 4A
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    if len(sequence) <= 1:
        return [sequence]
    sl = []
    for i in range(len(sequence)):
        for j in get_permutations(sequence[0:i] + sequence[i + 1:]):
            sl.append(sequence[i] + j)
    return sl


if __name__ == '__main__':
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'ok'
    print('Input:', example_input)
    print('Expected Output:', ['ok', 'ko'])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'orz'
    print('Input:', example_input)
    print('Expected Output:', ['orz', 'ozr', 'roz', 'rzo', 'zor', 'zro'])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'nice'
    print('Input:', example_input)
    print('Expected Output:',
          ['nice', 'niec', 'ncie', 'ncei', 'neic', 'neci', 'ince', 'inec', 'icne', 'icen', 'ienc', 'iecn', 'cnie', 'cnei',
           'cine', 'cien', 'ceni', 'cein', 'enic', 'enci', 'einc', 'eicn', 'ecni', 'ecin'])
    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)


