# Solution Times Backend

The aim of the web app is to allow end users to upload problemstatements that they face in everyday life to the website, and allow students to build solutions for these problems and upload their solutions which will be accessible to the end users. Students can use these problems as their semester or final year projects too. All this while allowing the community to sponsor and mentor a set of or a particular challenge.

### Users

On sign-up each user will be given a check-box array where they can select if they want to be end-user(upload problems), contestant/student(upload solutions), mentor, sponsor. All options can also be checked. From the user we require 
1. Email
2. First Name
3. Last Name
4. Date of birth
5. College Name (if applicable)
### Problemstatements

This is the core of the web app. Each problemstatement will allow a user, depending on their type(s) to either Mentor,sponsor, contest in a particular problemstatement. Hence each problem statement will have 3 buttons linked to it, which will be shown according to the type of user that is logged in! 

On this page we will also display problem statement details such as
1.  Total no of contestants for the problem statement
2. No of entries under General, Advanced and Legendary category 
3. Total no of mentors for the problem statement
4. Total no of sponsors for the problem statement
5. Total no of volunteering end users for the problem statement
6. Domain of the problem statement

##### Submitting a solution

Solutions when submitted will require the contestant to upload
1. A google drive url/github repo with their code
2. A video explanation of what their app does and how it solves the problem
3. A document with formal documentation
4. Link to solution (website or apk)
5. The category under which solution is submitted (G,A,L)

##### Sponsoring and Mentoring

Both these tasks will be on button click and they will be automatically added as mentor/sponsor for that particular problem statement and will be displayed on that problemchallenge specific page.

Sponsors/mentors will also have the option to sponsor/mentor multiple challenges from the home page. They can choose to sponsor/mentor all challenges in a patircular domain or more

#### End-users

The end users can upload a problem statement to the website but just putting in a youtube link, we get title and description from that link itself
