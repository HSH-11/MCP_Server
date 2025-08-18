def process_payment(order, payment_method):
    if payment_method == "credit_card" or payment_method == "bank_transfer":
        order["status"] = "paid"
        return "결제 완료"
    else:
        order["status"] = "failed"
        return "결제 실패"

def ship_order(order):
    order["status"] = "shipped"
    return "배송 시작"

def send_receipt(order):
    if order.get("status") == "paid":
        order["receipt_sent"] = True
        return "영수증 발송 완료"
    else:
        return "결제 미완료로 영수증 발송 불가"