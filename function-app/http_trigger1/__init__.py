import azure.functions as func
import requests
import logging
import json

app = func.FunctionApp()

@app.function_name(name="http_trigger1")
@app.route(route="http_trigger1", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)  # ✅ Fixed here
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing module registration request.')

    try:
        req_body = req.get_json()
        logging.info(f"Received request: {req_body}")

        # Validate required fields
        for field in ['email', 'module', 'action', 'date']:
            if field not in req_body:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    mimetype="application/json",
                    status_code=400
                )
        # POST to Django backend
        django_response = requests.post(
            "https://ardenthorizonuniversity-ehhscbggc0b0gzhm.uksouth-01.azurewebsites.net/send_registration_email/",
            json=req_body
        )

        return func.HttpResponse(
             json.dumps({
                "message": "Registration processed successfully.",
                "django_response": django_response.text
            }),
            mimetype="application/json",
            status_code=django_response.status_code
        )

    except Exception as e:
        logging.error(f"Error in Azure Function: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
