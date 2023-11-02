from worker import Worker, Delivery, Non_Delivery
import csv

class WorkerDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.database = self.read_workers_from_csv()

    def __str__(self):
        return '\n'.join(str(worker) for worker in self.database)

    def read_workers_from_csv(self):
        workers = []
        try:
            with open(self.filename, newline="") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    if row.get('duty'):
                        worker = Delivery(
                            row.get('name', None),
                            row.get('surname', None),
                            row.get('phoneNumber', None),
                            row.get('salary', None),
                            row.get('department', None),
                            row['duty']
                        )
                    elif row.get('jobTitle'):
                        worker = Non_Delivery(
                            row.get('name', None),
                            row.get('surname', None),
                            row.get('phoneNumber', None),
                            row.get('salary', None),
                            row.get('department', None),
                            row['jobTitle']
                        )
                    else:
                        worker = Worker(
                            row.get('name', None),
                            row.get('surname', None),
                            row.get('phoneNumber', None),
                            row.get('salary', None),
                            row.get('department', None)
                        )
                    workers.append(worker)
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
        return workers


    def create_worker_from_user_input(self, subclass=None):
        name = input("Name: ")
        surname = input("Surname: ")
        phoneNumber = input("Phone number: ")
        salary = input("Salary: ")
        department = input("Department: ")
        if subclass == Delivery:
            duty = input("Duty: ")
            a = Delivery(name, surname, phoneNumber, salary, department, duty)
        elif subclass == Non_Delivery:
            jobTitle = input("Job Title: ")
            a = Non_Delivery(name, surname, phoneNumber, salary, department, jobTitle)
        else:
            a = Worker(name, surname, phoneNumber, salary, department)
        self.add_worker_to_csv(a)
        return a

    def search_workers(self, key, value):
        valid_workers = []
        try:
            with open(self.filename, newline="") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    if row[key] == value:
                        worker = Worker(
                            row.get('name', None),
                            row.get('surname', None),
                            row.get('phoneNumber', None),
                            row.get('salary', None),
                            row.get('department', None),
                            row.get('duty', None),
                            row.get('jobTitle', None)
                        )
                        valid_workers.append(worker)
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
        return valid_workers

    def add_worker_to_csv(self, worker):
        self.database.append(worker)
        self.write_new_worker(worker)

    def delete_worker(self, worker_id):
        for worker in self.database:
            if worker.worker_id == worker_id:
                self.database.remove(worker)
                self.update_csv_file()
                print(f"Worker with ID {worker_id} has been deleted.")
                break
        else:
            print(f"Worker with ID {worker_id} not found.")

    def edit_worker(self, worker_id, param, value):
        for worker in self.database:
            if worker.worker_id == worker_id:
                if hasattr(worker, param):
                    setattr(worker, param, value)
                    self.update_csv_file()
                    print(f"Worker with ID {worker_id} has been updated.")
                    break
                else:
                    print(f"Parameter '{param}' not found in Worker.")
                    break
        else:
            print(f"Worker with ID {worker_id} not found.")

    def update_csv_file(self):
        try:
            with open(self.filename, 'w', newline='') as csvfile:
                fieldnames = ['name', 'surname', 'phoneNumber', 'salary', 'department', 'duty', 'jobTitle']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for worker in self.database:
                        row = {
                            'name': worker.name,
                            'surname': worker.surname,
                            'phoneNumber': worker.phoneNumber,
                            'salary': worker.salary,
                            'department': worker.department,
                        }
                        if isinstance(worker, Delivery):
                            row['duty'] = worker.duty
                            row['jobTitle'] = ''
                        elif isinstance(worker, Non_Delivery):
                            row['duty'] = ''
                            row['jobTitle'] = worker.jobTitle

                        writer.writerow(row)
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")

    def write_new_worker(self, worker):
        try:
            with open(self.filename, 'a', newline='') as csvfile:
                fieldnames = ['name', 'surname', 'phoneNumber', 'salary', 'department', 'duty', 'jobTitle']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                row = {
                    'name': worker.name,
                    'surname': worker.surname,
                    'phoneNumber': worker.phoneNumber,
                    'salary': worker.salary,
                    'department': worker.department,
                }

                if isinstance(worker, Delivery):
                    row['duty'] = worker.duty
                    row['jobTitle'] = ''
                elif isinstance(worker, Non_Delivery):
                    row['duty'] = ''
                    row['jobTitle'] = worker.jobTitle

                writer.writerow(row)

            print(f"Worker {worker.surname} added to the CSV file.")
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")

    def sort_by_param(self, param):
        self.database.sort(key=lambda worker: getattr(worker, param))
        self.update_csv_file()

        print(f"Database sorted by parameter '{param}'.")