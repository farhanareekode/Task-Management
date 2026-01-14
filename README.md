# Task-Management
Authentication & Roles

Super Admin

Full system control

Create, update, assign, delete tasks

View completion reports

Admin

Limited admin operations (if enabled)

User

View only their assigned tasks

Update task status (Pending → In Progress → Completed)

Submit completion report and worked hours

Authentication & Roles

Super Admin

Full system control

Create, update, assign, delete tasks

View completion reports

Admin

Limited admin operations (if enabled)

User

View only their assigned tasks

Update task status (Pending → In Progress → Completed)

Submit completion report and worked hours


backend/
│
├── admin_panel/
│   ├── templates/
│   │   └── admin_panel/
│   │       ├── base.html
│   │       ├── user_base.html
│   │       ├── tasks.html
│   │       ├── user_tasks.html
│   │       └── task_report.html
│   ├── views.py
│   ├── urls.py
│   └── models.py
│
├── accounts/
│   ├── views.py
│   ├── urls.py
│
├── backend/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
└── README.md
