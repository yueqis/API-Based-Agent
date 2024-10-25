# Estimate shipping costs

Using this method, we could calculate shipping costs for each shipping method that can be applied to the order. In this tutorial, the `flatrate` ($5 per item) and `tablerate` shipping methods are active.

**Endpoint:**
`POST <host>/rest/default/V1/carts/mine/estimate-shipping-methods`

**Headers:**
`Content-Type: application/json`
`Authorization: Bearer <customer token>`

**Payload:**
The payload contains the shipping address, for example: 
```json
{
  "address": {
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
    "customer_id": 4,
    "email": "jdoe@example.com",
    "telephone": "(512) 555-1111",
    "same_as_billing": 1
  }
}
```

**Response:**
The following response indicates that the cost for the `flatrate` shipping method is $15, and the cost for the `tablerate` shipping method is $5.

```json
[
  {
    "carrier_code": "flatrate",
    "method_code": "flatrate",
    "carrier_title": "Flat Rate",
    "method_title": "Fixed",
    "amount": 15,
    "base_amount": 15,
    "available": true,
    "error_message": "",
    "price_excl_tax": 15,
    "price_incl_tax": 15
  },
  {
    "carrier_code": "tablerate",
    "method_code": "bestway",
    "carrier_title": "Best Way",
    "method_title": "Table Rate",
    "amount": 5,
    "base_amount": 5,
    "available": true,
    "error_message": "",
    "price_excl_tax": 5,
    "price_incl_tax": 5
  }
]
```
