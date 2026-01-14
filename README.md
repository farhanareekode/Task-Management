<div>

<h1>🚀 Task Management System</h1>
<h2>▶️ Running the Project</h2>

<p align="left"><b>1. Clone the repository</b></p>
<pre>
git clone https://github.com/your-username/Task-Management.git
cd Task-Management
</pre>

<p align="left"><b>2. Create and activate virtual environment</b></p>
<pre>
python -m venv venv
source venv/bin/activate   <!-- Linux / Mac -->
venv\Scripts\activate      <!-- Windows -->
</pre>

<p align="left"><b>3. Install dependencies</b></p>
<pre>
pip install -r requirements.txt
</pre>

<p align="left"><b>4. Run database migrations</b></p>
<pre>
python manage.py makemigrations
python manage.py migrate
</pre>

<p align="left"><b>5. Create Super Admin</b></p>
<pre>
python manage.py createsuperuser
</pre>

<p align="left">
This account is the <b>Super Admin</b> and has full system control.
</p>

<p align="left"><b>6. Start the development server</b></p>
<pre>
python manage.py runserver
</pre>

<p>
Open browser and visit:<br>
<b>http://127.0.0.1:8000/</b>
</p>

<hr width="60%" />

<h2>👑 Super Admin Setup & Login</h2>

<p align="left">
1. Log in using the <b>Super Admin</b> credentials created with
<code>createsuperuser</code>.
</p>

<p align="left">
2. After login, you will be redirected to the <b>Super Admin Dashboard</b>.
</p>

<p align="left">
3. From the dashboard, the Super Admin can:
</p>

<p align="left">
✔ Create Admin accounts<br>
✔ Create User accounts<br>
✔ Assign roles and permissions<br>
✔ Create and assign tasks
</p>

<hr width="60%" />

<h2>🛠 Creating Admin Accounts</h2>

<p align="left">
1. Log in as <b>Super Admin</b>.
</p>

<p align="left">
2. Navigate to the <b>Admin Management</b> section.
</p>

<p align="left">
3. Create a new user and assign the role <b>Admin</b>.
</p>

<p align="left">
Admins can log in and manage tasks assigned to their users.
</p>

<hr width="60%" />

<h2>👤 Creating User Accounts</h2>

<p align="left">
1. Log in as <b>Super Admin</b> or <b>Admin</b> (if enabled).
</p>

<p align="left">
2. Navigate to the <b>User Management</b> section.
</p>

<p align="left">
3. Create a new user and assign tasks.
</p>

<p align="left">
Users can log in to:
</p>

<p align="left">
✔ View assigned tasks<br>
✔ Update task status<br>
✔ Submit completion reports<br>
✔ Log worked hours
</p>


<p>
A <b>role-based task management system</b> to assign tasks, track progress,  
and collect completion reports with worked hours.
</p>

<hr width="60%" />

<h2>✨ Features</h2>

<p>
🔐 Role-based authentication<br>
📋 Task creation & assignment<br>
⏱ Worked hours tracking<br>
📝 Completion reports<br>
📊 Progress monitoring
</p>

<hr width="60%" />

<h2>🔑 Authentication & Roles</h2>

<h3>👑 Super Admin</h3>

<p>
✔ Full system control<br>
✔ Create, update, assign, delete tasks<br>
✔ Manage admins and users<br>
✔ View all completion reports<br>
✔ Monitor worked hours system-wide
</p>

<h3>🛠 Admin</h3>

<p>
✔ Limited administrative access<br>
✔ View assigned users’ tasks<br>
✔ Assign tasks (if enabled)<br>
✔ Track progress<br>
✔ View completion reports
</p>

<h3>👤 User</h3>

<p>
✔ View only assigned tasks<br>
✔ Update task status<br>
<b>Pending → In Progress → Completed</b><br>
✔ Submit completion reports<br>
✔ Log worked hours
</p>

<hr width="60%" />

<h2>🔄 Task Workflow</h2>

<p>
Task Created → Assigned → In Progress → Completed → Report Submitted
</p>

<hr width="60%" />

<h2>🧱 Role Summary</h2>

<table align="center" border="1" cellpadding="8" cellspacing="0">
<tr>
<th>Role</th>
<th>Task Management</th>
<th>View Reports</th>
<th>Manage Users</th>
</tr>
<tr>
<td>Super Admin</td>
<td>Full</td>
<td>All</td>
<td>Yes</td>
</tr>
<tr>
<td>Admin</td>
<td>Limited</td>
<td>Assigned</td>
<td>No</td>
</tr>
<tr>
<td>User</td>
<td>No</td>
<td>No</td>
<td>No</td>
</tr>
</table>

<hr width="60%" />

<h2>🛠 Tech Stack</h2>

<p>
Django · PostgreSQL / SQLite · HTML · CSS
</p>

<hr width="60%" />

<p>
<b>License:</b> MIT
</p>

</div>
