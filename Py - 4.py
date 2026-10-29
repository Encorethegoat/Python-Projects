class student:
    def __init__(self, name, salary, work_location):
        self.name = name
        self.salary = salary
        self.work_location = work_location
class employee1:
    def __init__(self, name, salary, work_location):
        self.name = name
        self.salary = salary
        self.work_location = work_location
    def employee(self):
        print("Name: ", self.name)
        print("Salary: ", self.salary)
        print("Work Location: ", self.work_location)
class employee2:
    def __init__(self, name, salary, work_location):
        self.name = name
        self.salary = salary
        self.work_location = work_location
    def employee(self):
        print("Name: ", self.name)
        print("Salary: ", self.salary)
        print("Work Location: ", self.work_location)
class employee3:    
    def __init__(self, name, salary, work_location):
        self.name = name
        self.salary = salary
        self.work_location = work_location
    def employee(self):
        print("Name: ", self.name)
        print("Salary: ", self.salary)
        print("Work Location: ", self.work_location)

obj1 = employee1("Rudra", 50000, "Jharkhand")
obj2 = employee2("Hardik", 60000, "Rajasthan")
obj3 = employee3("Akshay Sir the goat ", 55000, "Heaven")
obj1.employee()
obj2.employee()
obj3.employee()
