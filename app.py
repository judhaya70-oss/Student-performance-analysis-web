from flask import Flask, render_template, request
import pandas as pd
app=Flask(__name__)
# Load dataset
data = pd.read_csv("students.csv")
print(data.columns.tolist())


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None

    if request.method == "POST":

        reg_no = request.form["student_id"]

        student_data = data[
            data["StudentID"].astype(str) == reg_no
        ]

        if student_data.empty:

            error = "Student not found. Please check the Student ID."

        else:

            student = student_data.iloc[0]

            subjects = [
                "Maths",
                "Physics",
                "Chemistry",
                "Python",
                "English"
            ]

            marks = {
                subject: int(student[subject])
                for subject in subjects
            }

            average = sum(marks.values()) / len(marks)

            strong_subjects = [
                subject
                for subject, mark in marks.items()
                if mark >= 75
            ]

            improvement_subjects = [
                subject
                for subject, mark in marks.items()
                if mark < 60
            ]

            if average >= 85:
                performance = "Excellent"
            elif average >= 75:
                performance = "Very Good"
            elif average >= 60:
                performance = "Good"
            else:
                performance = "Needs Improvement"

            previous_average = float(student["PreviousAverage"])

            difference = round(
                average - previous_average, 2
            )

            if difference > 2:
                trend = "Improving"
            elif difference < -2:
                trend = "Declining"
            else:
                trend = "Stable"

            recommendations = []

            for subject, mark in marks.items():

                if mark < 60:

                    recommendations.append(
                        f"Focus more on {subject} and practice regularly."
                    )

                elif mark < 75:

                    recommendations.append(
                        f"Try to improve your {subject} performance."
                    )

            result = {
                "id": student["StudentID"],
                "name": student["Name"],
                "semester": student["Semester"],
                "marks": marks,
                "average": round(average, 2),
                "attendance": student["Attendance"],
                "previous": previous_average,
                "difference": difference,
                "trend": trend,
                "performance": performance,
                "strong": strong_subjects,
                "improve": improvement_subjects,
                "recommendations": recommendations
            }

    return render_template(
        "index.html",
        result=result,
        error=error
    )


if __name__== "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
