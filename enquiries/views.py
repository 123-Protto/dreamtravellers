import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Enquiry
from datetime import datetime
from django.conf import settings

import sendgrid
from sendgrid.helpers.mail import Mail


# -------------------------------------------------------
#  CHATBOT REPLY API
# -------------------------------------------------------
@csrf_exempt
def chat_reply(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body.decode("utf-8"))
        user_msg = data.get("message", "").strip()
    except:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    if not user_msg:
        return JsonResponse({"reply": "Please type something."})

    msg = user_msg.lower()

    if "hi" in msg or "hello" in msg:
        reply = "Hello! 👋 How can I help you plan your trip?"
    elif "price" in msg:
        reply = "Prices depend on dates, hotel category & number of travellers. When are you planning to travel?"
    elif "package" in msg:
        reply = "We offer Kerala | Coorg | Mysore | Kanyakumari | Vagamon and many custom tour packages!"
    else:
        reply = "Thank you! Please share more details so I can help you better."

    return JsonResponse({"reply": reply})



# -------------------------------------------------------
#  SENDGRID EMAIL NOTIFICATION
# -------------------------------------------------------
def notify_admin(enquiry):
    """
    Sends enquiry details to admin email using SendGrid.
    """

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    html_content = f"""
        <h2>New Travel Enquiry Received</h2>

        <p><strong>Name:</strong> {enquiry.name}</p>
        <p><strong>Phone:</strong> {enquiry.phone}</p>
        <p><strong>Email:</strong> {enquiry.email}</p>

        <p><strong>Starting Location:</strong> {enquiry.starting_location}</p>
        <p><strong>Destination:</strong> {enquiry.planned_destination}</p>
        <p><strong>Travel Date:</strong> {enquiry.travel_date}</p>
        <p><strong>Travel Group:</strong> {enquiry.travel_group}</p>

        <p><strong>Nights:</strong> {enquiry.nights}</p>
        <p><strong>Adults:</strong> {enquiry.adults}</p>
        <p><strong>Children:</strong> {enquiry.children}</p>

        <p><strong>Hotel Category:</strong> {enquiry.hotel_category}</p>
        <p><strong>Transportation:</strong> {enquiry.transportation}</p>

        <p><strong>Notes:</strong><br>{enquiry.extra_requirement}</p>

        <hr>
        <p>Dream Travellers – Admin Notification</p>
    """

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails="dreamtravellers.ta@gmail.com",
        subject="📩 New Travel Enquiry Received",
        html_content=html_content,
    )

    try:
        sg.send(message)
        print("SendGrid Email Sent Successfully!")
    except Exception as e:
        print("SendGrid Email Failed:", e)



# -------------------------------------------------------
#  SAVE ENQUIRY API
# -------------------------------------------------------
@csrf_exempt
def save_enquiry(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=400)

    # Parse JSON
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    try:
        # Convert travel date safely
        travel_date_raw = data.get("travel_date")
        travel_date = None

        if travel_date_raw:
            try:
                travel_date = datetime.strptime(travel_date_raw, "%Y-%m-%d").date()
            except:
                travel_date = None

        # Save enquiry
        enquiry = Enquiry.objects.create(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            starting_location=data.get("starting_location", ""),
            planned_destination=data.get("planned_destination", ""),
            travel_date=travel_date,
            travel_group=data.get("travel_group", ""),
            nights=data.get("nights", 0),
            adults=data.get("adults", 0),
            children=data.get("children", 0),
            hotel_category=data.get("hotel_category", ""),
            transportation=data.get("transportation", ""),
            extra_requirement=data.get("extra_requirement", "")
        )

        # Try sending email
        try:
            notify_admin(enquiry)
        except Exception as mail_error:
            print("Email sending failed:", mail_error)

        return JsonResponse({"status": "ok", "id": enquiry.id})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
