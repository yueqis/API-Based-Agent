# Set shipping and billing information

In this call, you can specify or change the shipping and billing addresses, as well as the selected `carrier_code` and `method_code`. `carrier_code` could be either `tablerate` or `flatrate`. `method_code` could be either `bestway`, `tablerate`, or `flatrate`.

This API returns a list of payment options and calculates the order totals.

**Endpoint:**
`POST <host>/rest/default/V1/carts/mine/shipping-information`

**Headers:**
`Content-Type: application/json`
`Authorization: Bearer <customer token>`

**Payload:**
```json
{
  "addressInformation": {
    "shipping_address": {
      "region": "New York",
      "region_id": 43,
      "region_code": "NY",
      "country_id": "US",
      "street": [
        "123 Oak Ave"
      ],
      "postcode": "10577",
      "city": "Purchase",
      "firstname": "Jane",
      "lastname": "Doe",
      "email": "jdoe@example.com",
      "telephone": "512-555-1111"
    },
    "billing_address": {
      "region": "New York",
      "region_id": 43,
      "region_code": "NY",
      "country_id": "US",
      "street": [
        "123 Oak Ave"
      ],
      "postcode": "10577",
      "city": "Purchase",
      "firstname": "Jane",
      "lastname": "Doe",
      "email": "jdoe@example.com",
      "telephone": "512-555-1111"
    },
    "shipping_carrier_code": "tablerate",
    "shipping_method_code": "bestway"
  }
}
```

**Response:**
The subtotal of the order is $160, and shipping charges are $5. The grand total is $165.

The available payment methods are `banktransfer` and `checkmo`. The customer will specify a payment method in the next step.
```json
{
  "payment_methods": [
    {
      "code": "cashondelivery",
      "title": "Cash On Delivery"
    },
    {
      "code": "banktransfer",
      "title": "Bank Transfer Payment"
    },
    {
      "code": "purchaseorder",
      "title": "Purchase Order"
    },
    {
      "code": "checkmo",
      "title": "Check / Money order"
    }
  ],
  "totals": {
    "grand_total": 165,
    "base_grand_total": 165,
    "subtotal": 160,
    "base_subtotal": 160,
    "discount_amount": 0,
    "base_discount_amount": 0,
    "subtotal_with_discount": 160,
    "base_subtotal_with_discount": 160,
    "shipping_amount": 5,
    "base_shipping_amount": 5,
    "shipping_discount_amount": 0,
    "base_shipping_discount_amount": 0,
    "tax_amount": 0,
    "base_tax_amount": 0,
    "weee_tax_applied_amount": null,
    "shipping_tax_amount": 0,
    "base_shipping_tax_amount": 0,
    "subtotal_incl_tax": 160,
    "shipping_incl_tax": 5,
    "base_shipping_incl_tax": 5,
    "base_currency_code": "USD",
    "quote_currency_code": "USD",
    "items_qty": 4,
    "items": [
      {
        "item_id": 6,
        "price": 22,
        "base_price": 22,
        "qty": 1,
        "row_total": 22,
        "base_row_total": 22,
        "row_total_with_discount": 0,
        "tax_amount": 0,
        "base_tax_amount": 0,
        "tax_percent": 0,
        "discount_amount": 0,
        "base_discount_amount": 0,
        "discount_percent": 0,
        "price_incl_tax": 22,
        "base_price_incl_tax": 22,
        "row_total_incl_tax": 22,
        "base_row_total_incl_tax": 22,
        "options": "[]",
        "weee_tax_applied_amount": null,
        "weee_tax_applied": null,
        "name": "Radiant Tee-M-Orange"
      },
      {
        "item_id": 7,
        "price": 18,
        "base_price": 18,
        "qty": 1,
        "row_total": 18,
        "base_row_total": 18,
        "row_total_with_discount": 0,
        "tax_amount": 0,
        "base_tax_amount": 0,
        "tax_percent": 0,
        "discount_amount": 0,
        "base_discount_amount": 0,
        "discount_percent": 0,
        "price_incl_tax": 18,
        "base_price_incl_tax": 18,
        "row_total_incl_tax": 18,
        "base_row_total_incl_tax": 18,
        "options": "[{\"value\":\"Advanced Pilates & Yoga (Strength)\",\"label\":\"Downloads\"}]",
        "weee_tax_applied_amount": null,
        "weee_tax_applied": null,
        "name": "Advanced Pilates & Yoga (Strength)"
      },
      {
        "item_id": 8,
        "price": 68,
        "base_price": 68,
        "qty": 1,
        "row_total": 68,
        "base_row_total": 68,
        "row_total_with_discount": 0,
        "tax_amount": 0,
        "base_tax_amount": 0,
        "discount_amount": 0,
        "base_discount_amount": 0,
        "discount_percent": 0,
        "price_incl_tax": 68,
        "base_price_incl_tax": 68,
        "row_total_incl_tax": 68,
        "base_row_total_incl_tax": 68,
        "options": "[{\"value\":\"1 x Sprite Stasis Ball 65 cm <span class=\\\"price\\\">$27.00<\\/span>\",\"label\":\"Sprite Stasis Ball\"},{\"value\":\"1 x Sprite Foam Yoga Brick <span class=\\\"price\\\">$5.00<\\/span>\",\"label\":\"Sprite Foam Yoga Brick\"},{\"value\":\"1 x Sprite Yoga Strap 8 foot <span class=\\\"price\\\">$17.00<\\/span>\",\"label\":\"Sprite Yoga Strap\"},{\"value\":\"1 x Sprite Foam Roller <span class=\\\"price\\\">$19.00<\\/span>\",\"label\":\"Sprite Foam Roller\"}]",
        "weee_tax_applied_amount": null,
        "weee_tax_applied": null,
        "name": "Sprite Yoga Companion Kit"
      },
      {
        "item_id": 13,
        "price": 52,
        "base_price": 52,
        "qty": 1,
        "row_total": 52,
        "base_row_total": 52,
        "row_total_with_discount": 0,
        "tax_amount": 0,
        "base_tax_amount": 0,
        "tax_percent": 0,
        "discount_amount": 0,
        "base_discount_amount": 0,
        "discount_percent": 0,
        "price_incl_tax": 52,
        "base_price_incl_tax": 52,
        "row_total_incl_tax": 52,
        "base_row_total_incl_tax": 52,
        "options": "[{\"value\":\"Gray\",\"label\":\"Color\"},{\"value\":\"S\",\"label\":\"Size\"}]",
        "weee_tax_applied_amount": null,
        "weee_tax_applied": null,
        "name": "Chaz Kangeroo Hoodie"
      }
    ],
    "total_segments": [
      {
        "code": "subtotal",
        "title": "Subtotal",
        "value": 160
      },
      {
        "code": "shipping",
        "title": "Shipping & Handling (Best Way - Table Rate)",
        "value": 5
      },
      {
        "code": "tax",
        "title": "Tax",
        "value": 0,
        "extension_attributes": {
          "tax_grandtotal_details": []
        }
      },
      {
        "code": "grand_total",
        "title": "Grand Total",
        "value": 165,
        "area": "footer"
      }
    ]
  }
}
```
