from datetime import datetime
from django.conf import settings

from .forms import PaymentForm
from .vnpay import vnpay


def create_payment(request, order_uuid, total_payment):
    timestamp = datetime.now()
    vnpay_payment_url = ""
    form = PaymentForm(
        {
            "order_id": order_uuid,
            "amount": total_payment,
            "order_type": "fashion",
            "language": "vn",
            "bank_code": "",
            "order_desc": f"Thanh toan don hang thoi gian: {timestamp.strftime("%Y%m%d%H%M%S")}",
        }
    )
    if form.is_valid():

        order_type = form.cleaned_data["order_type"]
        order_id = form.cleaned_data["order_id"]
        amount = form.cleaned_data["amount"]
        order_desc = form.cleaned_data["order_desc"]
        bank_code = form.cleaned_data["bank_code"]
        language = form.cleaned_data["language"]
        ipaddr = get_client_ip(request)

        vnp = vnpay()
        vnp.requestData["vnp_Version"] = "2.1.0"
        vnp.requestData["vnp_Command"] = "pay"
        vnp.requestData["vnp_TmnCode"] = settings.VNPAY_TMN_CODE
        vnp.requestData["vnp_Amount"] = amount * 100
        vnp.requestData["vnp_CurrCode"] = "VND"
        vnp.requestData["vnp_TxnRef"] = order_id
        vnp.requestData["vnp_OrderInfo"] = order_desc
        vnp.requestData["vnp_OrderType"] = order_type

        if language and language != "":
            vnp.requestData["vnp_Locale"] = language
        else:
            vnp.requestData["vnp_Locale"] = "vn"

        if bank_code and bank_code != "":
            vnp.requestData["vnp_BankCode"] = bank_code

        vnp.requestData["vnp_CreateDate"] = timestamp.strftime("%Y%m%d%H%M%S")
        vnp.requestData["vnp_IpAddr"] = ipaddr
        vnp.requestData["vnp_ReturnUrl"] = settings.VNPAY_RETURN_URL
        vnpay_payment_url = vnp.get_payment_url(
            settings.VNPAY_PAYMENT_URL,
            settings.VNPAY_HASH_SECRET_KEY,
        )

    return vnpay_payment_url


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def payment_return_handler(request):
    inputData = request.GET
    response_data = {"res_code": ""}

    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData["vnp_TxnRef"]
        amount = int(inputData["vnp_Amount"]) / 100
        order_desc = inputData["vnp_OrderInfo"]
        vnp_TransactionNo = inputData["vnp_TransactionNo"]
        vnp_ResponseCode = inputData["vnp_ResponseCode"]
        vnp_TmnCode = inputData["vnp_TmnCode"]
        vnp_PayDate = inputData["vnp_PayDate"]
        vnp_BankCode = inputData["vnp_BankCode"]
        vnp_CardType = inputData["vnp_CardType"]

        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                response_data = {
                    "res_code": vnp_ResponseCode,
                    "order_id": order_id,
                    "order_desc": order_desc,
                    "amount": amount,
                    "bank_code": vnp_BankCode,
                    "pay_date": vnp_PayDate,
                    "vnp_TransactionNo": vnp_TransactionNo,
                    "vnp_TmnCode": vnp_TmnCode,
                    "vnp_CardType": vnp_CardType,
                }

    return response_data
