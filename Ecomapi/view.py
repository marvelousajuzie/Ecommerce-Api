from rest_framework import response




def initial_payment(amount, email, redirect_url):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer{settings.FLW_SEC_KEY}"
    }

    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": redirect_url,
        "meta": {
            "consumers_id": 23,
            "consumers_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": email,
            "phonenumber": "080*****81",
            "name": "Marvelous Ajuzie",
        },
        "customizations":
        {
            "title": "pied piper Payments",
            "logo": "http://www.piedpiper.com/app/theme/joystick-v27/images/logo-png",
        }
    }

    try:
        response = request.post(url, headers= headers, json= data)
        response_data = response.json()
        return Response(response_data)
    except requests.exceptions.RequestException as err:
        print("The payment didint go through")
        return Response({'error': str(err)}, status = 500)