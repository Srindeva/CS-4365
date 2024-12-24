import sys
from io import StringIO
from clause import Clause
from resolution import Resolution

#For cross checking correct output
def grader():
    stdout_capture = StringIO()
    original_stdout = sys.stdout  
    sys.stdout = stdout_capture  
    
    sys.argv = ['main.py', 'demo.kb']

    kb_file = sys.argv[1]
    solver = Resolution()
    solver.load_kb(kb_file)
    solver.prove()
    
    sys.stdout = original_stdout    
    stdout_capture.seek(0)
    correct = True
    print(stdout_capture)
    with("demo.out", "r") as output_file:
        for i in len(output_file):
            if not (stdout_capture.seek(i) == output_file.strip()):
                correct = False
    print(kb_file, ": ", correct)

if __name__ == '__main__':
    #Example inputs for debugging
    #sys.argv = ['main.py', 'demo.kb']
    kb_file = sys.argv[1]
    solver = Resolution()
    solver.load_kb(kb_file)
    solver.prove()
