# Create a cart

**Endpoint:**
`POST <host>/rest/default/V1/carts/mine`

**Headers:**
`Content-Type: application/json`
`Authorization: Bearer <customer token>`

**Response:**
The response is the `quoteId`. 
To use any other APIs related to carts, you should first call this API to obtain the `quoteId` of the cart using this API. Other APIs related to `carts` will require this `quoteId`.
Note: Some calls might refer to this parameter as the `cartId`.
