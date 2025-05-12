import azure.functions as func
import requests
import logging

app = func.FunctionApp()

@app.function_name(name="sendConfirmationEmail")
@app.route(route="sendConfirmationEmail", auth_level=func.AuthLevel.Function)
def send_confirmation_email(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function: Processing email confirmation request.')

    try:
        req_body = req.get_json()

        # Validate required fields
        for field in ['email', 'module', 'action', 'date']:
            if field not in req_body:
                return func.HttpResponse(f"Missing required field: {field}", status_code=400)

        # POST to your Django backend
        django_response = requests.post(
            "http://localhost:8000/send-registration-email/",  # Update if Django is hosted elsewhere
            json=req_body
        )

        return func.HttpResponse(
            f"Django response: {django_response.text}",
            status_code=django_response.status_code
        )

    except Exception as e:
        logging.error(f"Error in Azure Function: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
