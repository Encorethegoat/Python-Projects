""" Write a program to read the ages of 10 students and display the highest """
ages = list(map(int, input("Enter the ages of 10 students separated by spaces: ").split()))
print("The highest age is:", max(ages))
ages.sort()
print("Highest age:", ages[-1])

""" Write a program to read the salaries of 10 employees and display the highest after giving 10% of bonus to each employee """
salary = list(map(int, input("Enter the salaries of 10 employees separated by spaces: ").split()))
for i in range(len(salary)):
    salary[i] += salary[i] * 0.10 

print("The highest salary is:", max(salary))

