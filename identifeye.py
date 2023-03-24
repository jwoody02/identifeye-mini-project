# import packages
import os
import sys

# class with dictionary of patients and exams
class Service:
    def __init__(self):
        self.patients = {}
        self.exams = {}
    
    # add patient
    def add_patient(self, id, name):
        self.patients[id] = name
    
    # delete patient
    def delete_patient(self, id):
        if id in self.patients:
            del self.patients[id]

    # add exam
    def add_exam(self, patient_id, exam_id):
        if patient_id in self.patients:
            self.exams[exam_id] = patient_id
        else:
            print("Warning: Patient with ID '" + str(patient_id) + "' does not exist, skipping..")
    
    # get exams
    def get_exams(self, patient_id):
        if patient_id in self.patients:
            return [exam for exam in self.exams if self.exams[exam] == patient_id]
        else:
            print("Warning: Patient with ID '" + str(patient_id) + "' does not exist, skipping..")
            return []
        
    # get patients:
    def get_all_patients(self):
        return self.patients
    
# parent instruction class
class Instruction:
    def __init__(self, command, service):
        self.service = service
        self.command = command

        # check for instruction type
        if "patient" in self.command.lower():
            # create patient instruction
            PatientInstruction(self.command, self.service)
        elif "exam" in self.command.lower():
            # create exam instruction
            ExamInstruction(self.command, self.service)
        else:
            print("Unrecognized instruction '" + str(self.command) + "'")

# patient subclass
class PatientInstruction():
    def __init__(self, command, service):
        self.service = service
        # parse command arguments
        _cmd = command.split(" ")[0]
        _args = command.split(" ")[1:]

        # run add and delete functions appropriately
        if _cmd.lower() == "add":
            self.add(_args[1:])
        elif _cmd.lower() == "del":
            self.delete(_args[1:])
        else:
            print("Invalid command '" + str(_cmd) + "'")
    
    def add(self, args):
        # check if patient already exists, if not, add
        if args[0] in self.service.patients:
            print("Warning: Patient with ID '" + str(args[0]) + "' already exists, skipping..")
        else:
            # use join to rejoin name if it has spaces
            self.service.add_patient(args[0], ' '.join(args[1:]))

    def delete(self, args):
        # check if patient exists, if so, delete
        if args[0] in self.service.patients:
            self.service.delete_patient(args[0])
        else:
            print("Warning: Patient with ID '" + str(args[0]) + "' does not exist, skipping..")

# exam subclass
class ExamInstruction():
    def __init__(self, command, service):
        self.service = service
        # parse command arguments
        _cmd = command.split(" ")[0]
        _args = command.split(" ")[1:]

        # run add and delete functions appropriately
        if _cmd.lower() == "add":
            self.add(_args[1:])
        elif _cmd.lower() == "del":
            self.delete(_args[1:])
        else:
            print("Invalid command '" + str(_cmd) + "'")
    
    # add exam
    def add(self, args):
        # check if exam already exists, if not, add
        if args[0] in self.service.exams:
            print("Warning: Exam with ID '" + str(args[0]) + "' already exists, skipping..")
        else:
            self.service.add_exam(args[0], args[1])
    
    # delete exam
    def delete(self, args):
        # check if exam exists, if so, delete
        if args[0] in self.service.exams:
            del self.service.exams[args[0]]
        else:
            print("Warning: Exam with ID '" + str(args[0]) + "' does not exist, skipping..")

# main
if __name__ == "__main__":
    service = Service()
    # check for and read input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if os.path.exists(input_file):
            with open(input_file, "r") as f:
                for line in f:
                    Instruction(line.strip(), service)
            # print summary:
            print("Summary:")
            print("========================================")
            for patient in service.get_all_patients():
                print("Name: " + str(service.patients[patient]) + ", ID: " + str(patient) + ", Exam Count: " + str(len(service.get_exams(patient))))
            print("========================================")
        else:
            print("Error: Input file '" + str(input_file) + "' does not exist")
    else:
        print("Usage: python identifeye.py <input_file>\nUse example.txt for an example")