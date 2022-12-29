import difflib
import argparse

def main(fileOne, fileTwo, outputFile):

    print('File of the left: ', fileOne)
    print('File on the right: ', fileTwo)
    f = open(f"output/{outputFile}", "a")
    with open(fileOne, 'r') as leftFile:
        with open(fileTwo, 'r') as rightFile:
            diff = difflib.unified_diff(
                leftFile.readlines(),
                rightFile.readlines(),
                fromfile=str(leftFile),
                tofile=str(rightFile),
            )

            for line in diff:
                f.write(str(line.replace("<_io.TextIOWrapper name='", "").replace("' mode='r' encoding='cp1252'>", "")))

    print('Done')
    print('Output file: ', outputFile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--left', '-l', help="Left file name", type= str)
    parser.add_argument('--right', '-r', help="Right file name", type= str)
    parser.add_argument('--out', '-o', help="output file name", type= str)
    args = parser.parse_args()
    main(args.left, args.right, args.out)

