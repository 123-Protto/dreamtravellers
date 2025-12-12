import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Enquiry
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings


# ---------------- CHATBOT REPLY API ---------------- #
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
        reply = "We offer Kerala, Coorg, Mysore, Kanyakumari, Vagamon and many custom tour packages!"
    else:
        reply = "Thank you! Please share more details so I can help you better."

    return JsonResponse({"reply": reply})



# ---------------- ADMIN EMAIL NOTIFICATION ---------------- #
def notify_admin(enquiry):
    subject = "📩 New Travel Enquiry Received"
    message = f"""
A new enquiry has been submitted.

Name: {enquiry.name}
Phone: {enquiry.phone}
Email: {enquiry.email}

Starting Location: {enquiry.starting_location}
Destination: {enquiry.planned_destination}
Travel Date: {enquiry.travel_date}
Travel Group: {enquiry.travel_group}

Nights: {enquiry.nights}
Adults: {enquiry.adults}
Children: {enquiry.children}

Hotel Category: {enquiry.hotel_category}
Transportation: {enquiry.transportation}

Notes:
{enquiry.extra_requirement}

-----------------------------------
Dream Travellers • Admin Notification
"""

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ["dreamtravellers.ta@gmail.com"],
            fail_silently=False
        )
        print("Email notification sent.")
    except Exception as e:
        print("Email sending failed:", e)



# ---------------- SAVE ENQUIRY API ---------------- #
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
        # Convert travel_date safely
        travel_date_raw = data.get("travel_date")
        travel_date = None
        if travel_date_raw:
            try:
                travel_date = datetime.strptime(travel_date_raw, "%Y-%m-%d").date()
            except:
                travel_date = None

        # Create enquiry
        enquiry = Enquiry.objects.create(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            starting_location=data.get("starting_location", ""),
            planned_destination=data.get("planned_destination", ""),
            travel_date=travel_date,
            travel_group=data.get("travel_group", ""),
            nights=data.get("nights", ""),
            adults=data.get("adults", ""),
            children=data.get("children", ""),
            hotel_category=data.get("hotel_category", ""),
            transportation=data.get("transportation", ""),
            extra_requirement=data.get("extra_requirement", "")
        )

        # Safe email sending
        try:
            notify_admin(enquiry)
        except Exception as mail_error:
            print("Email sending failed:", mail_error)

        return JsonResponse({"status": "ok", "id": enquiry.id})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
