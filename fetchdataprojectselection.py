import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:\\python_1\\pythonProject\\telecom-tower-performance-1-firebase-adminsdk-76b3k-265f93b36b.json')  # Update with your service account key
firebase_admin.initialize_app(cred)
db = firestore.client()

def fetch_employees(circle_name):
    employees = []
    # Query Firestore for employees with the specified circle_name
    docs = db.collection('users').where('circle_name', '==', circle_name).get()
    for doc in docs:
        employee_name = doc.to_dict().get('employee_Name')
        employees.append(employee_name)
    return employees

# Example usage
if __name__ == '__main__':
    circle_name = 'Maharashtra'  # Replace with the selected circle name
    employees = fetch_employees(circle_name)
    print("Employees in Maharashtra circle:", employees)


