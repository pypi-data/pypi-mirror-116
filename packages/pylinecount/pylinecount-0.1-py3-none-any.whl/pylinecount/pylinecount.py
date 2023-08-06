import os

def count_lines(path):
    count = 0

    for folder, _, files in os.walk('.'):
        for f in files:
            if f.endswith('.py'):
                with open(os.path.join(folder, f)) as code:
                    for line in code:
                        if line.strip() != '':
                            count += 1

    print(f'Counted {count} lines as codes and comments in .py files')

if __name__ == '__main__':
    count_lines('.')