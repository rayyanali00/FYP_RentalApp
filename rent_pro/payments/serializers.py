from rest_framework import serializers
from products.models import Order
"""
address: "Karachi, Pakistan"
city: "Karachi"
country: "Pakistan"
deliever_at: "2021-12-30"
email: "steve@email.com"
id: 48
is_accepted: "Accept"
order_id: "3ab0b3bf-d334-472a-9392-4d7fbdbcba65"
ordered_at: "2021-12-30T15:33:14.691949Z"
payment_process: "pending"
state: "Sindh"
status: "Pending"
total_amount: 110
user: 6
your_bid_total: 90
zip_code: "75290"
"""

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("order_id","email","your_bid_total","payment_process")