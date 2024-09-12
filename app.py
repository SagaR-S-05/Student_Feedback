from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key

# MySQL Connection Configuration
conn = mysql.connector.connect(
    user='root', password='Sagar11suma#', host='localhost', database='Survey'
)

# Route to display feedback form
@app.route('/', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        # Collecting form data for 5 subjects
        for i in range(1, 6):
            TeacherName = request.form[f'teacher_name_{i}']
            Subject = request.form[f'subject_{i}']
            Punctuality = request.form[f'punctuality_{i}']
            Knowledge = request.form[f'knowledge_{i}']
            Comm = request.form[f'communication_{i}']
            Rating = request.form[f'rating_{i}']

            # Inserting data into MySQL database
            cursor = conn.cursor()
            insert_stmt = (
                "INSERT INTO FEEDBACK (TEACHER_NAME, SUBJECT, PUNCTUALITYRATING_OUT_OF_5, KNOWLEDGEOFSUBJECT_OUT_OF_5, COMMUNICATIONSKILLS_OUT_OF_5, FINALRATING_OUT_OF_5) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            data = (TeacherName, Subject, Punctuality, Knowledge, Comm, Rating)

            try:
                cursor.execute(insert_stmt, data)
                conn.commit()
            except Exception as e:
                conn.rollback()
                flash(f'Error submitting feedback for subject {i}: {e}', 'error')
                return redirect(url_for('feedback_form'))

        flash('Feedback submitted successfully for all subjects!', 'success')
        return redirect(url_for('feedback_form'))

    return render_template('feedback_form.html')

if __name__ == '__main__':
    app.run(debug=True)