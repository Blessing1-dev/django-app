import azure.functions as func
import logging
import json
import os
import datetime
import requests

def write_email_to_file(to_email, subject, body, email_folder="emails"):
    if not os.path.exists(email_folder):
        os.makedirs(email_folder)

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    safe_email = to_email.replace("@", "_at_").replace(".", "_")
    filename = f"email_{timestamp}_{safe_email}.txt"
    filepath = os.path.join(email_folder, filename)

    content = f"To: {to_email}\nSubject: {subject}\n\n{body}"
    with open(filepath, "w") as f:
        f.write(content)
    logging.info(f"Email written to: {filepath}")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing module registration request.')

    try:
        req_body = req.get_json()
        logging.info(f"Received request: {req_body}")

        required_fields = ['email', 'student_name', 'module', 'action', 'date']
        for field in required_fields:
            if field not in req_body:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    mimetype="application/json",
                    status_code=400
                )

        student_email = req_body['email']
        student_name = req_body['student_name']
        module = req_body['module']
        action = req_body['action']
        date = req_body['date']

        # Email contents
        student_subject = f"You have successfully {action}ed for {module}"
        student_body = (
            f"Hi {student_name},\n\n"
            f"You have successfully {action}ed for {module} on {date}.\n\n"
            f"Regards,\nUniversity Team"
        )

        admin_email = "admin@university.edu"
        admin_subject = f"Student {action}ed for {module}"
        admin_body = f"Student {student_name} ({student_email}) has just {action}ed for {module}."

        write_email_to_file(student_email, student_subject, student_body)
        write_email_to_file(admin_email, admin_subject, admin_body)

        # Optional Django notification
        try:
            django_response = requests.post(
                "https://ardenthorizonuniversity-ehhscbggc0b0gzhm.uksouth-01.azurewebsites.net/send_registration_email/",
                json=req_body
            )
            django_response_text = django_response.text
            django_status = django_response.status_code
        except Exception as e:
            logging.warning(f"Failed to contact Django backend: {e}")
            django_response_text = str(e)
            django_status = 500

        return func.HttpResponse(
            json.dumps({
                "message": f"Emails for '{action}' written successfully.",
                "django_response": django_response_text
            }),
            mimetype="application/json",
            status_code=django_status
        )

    except Exception as e:
        logging.error(f"Azure Function error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
