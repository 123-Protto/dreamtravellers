import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Enquiry
from datetime import datetime


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



# ---------------- SAVE ENQUIRY API ---------------- #
@csrf_exempt
def save_enquiry(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=400)

    # Parse JSON safely
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    try:
        # Convert date safely
        travel_date_raw = data.get("travel_date")
        travel_date = None
        if travel_date_raw:
            try:
                travel_date = datetime.strptime(travel_date_raw, "%Y-%m-%d").date()
            except:
                travel_date = None  # don't break saving

        enquiry = Enquiry.objects.create(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),

            # Package info
            selected_package=data.get("selected_package", ""),

            # Travel details
            starting_location=data.get("starting_location", ""),
            travel_date=travel_date,
            travel_group=data.get("travel_group", ""),

            nights=int(data.get("nights") or 1),
            adults=int(data.get("adults") or 1),
            children=int(data.get("children") or 0),

            hotel_category=data.get("hotel_category", ""),
            transportation=data.get("transportation", ""),

            extra_requirement=data.get("extra_requirement", "")
        )

        return JsonResponse({"status": "ok", "id": enquiry.id})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
