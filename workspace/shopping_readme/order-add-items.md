# Add items to the cart

## Add a simple product to a cart

To add a simple product to a cart, you must provide a `sku` of a product, the quantity of the product, and the quote ID of your cart, which was generated when the cart was created.

The `sku` of a product, if not provided, could be obtained using the `GET /V1/products` endpoint. If you have the name of the product, the you could use `GET /V1/products` to search explicitly for products that have names matching your desired product name.

The following example adds an orange medium-sized Radiant women's t-shirt (`sku`: `WS12-M-Orange`) to the cart.

**Endpoint:**
`POST <host>/rest/default/V1/carts/mine/items`

**Headers:**
`Content-Type: application/json`
`Authorization: Bearer <customer token>`

**Payload:**
```json
{
  "cartItem": {
    "sku": "WS12-M-Orange",
    "qty": 1,
    "quote_id": quote_id
  }
}
```

**Response:**
```json
{
  "item_id": 7,
  "sku": "WS12-M-Orange",
  "qty": 1,
  "name": "Radiant Tee-M-Orange",
  "price": 19.99,
  "product_type": "simple",
  "quote_id": quote_id
}
```

## Add a downloadable product to a cart

The requirements for adding a downloadable product to a cart are the same as a simple product. You must specify the `sku`, the quantity, and quote ID.

The following example adds the downloadable product Advanced Pilates & Yoga (`sku`: 240-LV08)

**Endpoint:**
`POST <host>/rest/default/V1/carts/mine/items`

**Headers:**
`Content-Type: application/json`
`Authorization: Bearer <customer token>`

**Payload:**
```json
{
  "cartItem": {
    "sku": "240-LV08",
    "qty": 1,
    "quote_id": quote_id
  }
}
```

**Response:**
```json
{
  "item_id": 8,
  "sku": "240-LV08",
  "qty": 1,
  "name": "Advanced Pilates & Yoga (Strength)",
  "price": 18,
  "product_type": "downloadable",
  "quote_id": quote_id,
  "product_option": {
    "extension_attributes": {
      "downloadable_option": {
        "downloadable_links": [
          5
        ]
      }
    }
  }
}
```

## Add a configurable product to a cart

To add a configurable product to a cart, you must specify the `sku` as well as the set of `option_id`/`option_value` pairs that make the product configurable.

In this example, we'll add the Chaz Kangeroo Hoodie (`sku: MH01`) configurable product to the cart. This product comes in three colors (black, gray, and orange) and five sizes (XS, S, M, L, XL). For the Chaz Kangeroo Hoodie, the `option_id` values for Size and Color are `141` and `93`, respectively. You can use the `GET /V1/configurable-products/:sku/options/all` call to determine the `option_id` values for the given SKU.

The `GET /V1/configurable-products/:sku/children` call returns information about each combination of color and size, 15 in all for `MH01`. The following sample shows the returned values for `size` and `color` for a small gray Chaz Kangeroo Hoodie.

```json
{
  "custom_attributes": [
    {
      "attribute_code": "size",
      "value": "168"
    },
    {
      "attribute_code": "color",
      "value": "52"
    }
  ]
}
```

We now know the values for `option_value` for `size` and `color` are `168` and `52`, so we're ready to add the product to the cart.

**Endpoint:**
`POST <host>/rest/default/V1/carts/mine/items`

**Headers:**
`Content-Type: application/json`
`Authorization: Bearer <customer token>`

#### Payload
```json
{
  "cartItem": {
    "sku": "MH01",
    "qty": 1,
    "quote_id": quote_id,
    "product_option": {
      "extension_attributes": {
        "configurable_item_options": [
          {
            "option_id": "93",
            "option_value": 52
          },
          {
            "option_id": "141",
            "option_value": 168
          }
        ]
      }
    },
    "extension_attributes": {}
  }
}
```

#### Response
```json
{
  "item_id": 13,
  "sku": "MH01-S-Gray",
  "qty": 1,
  "name": "Chaz Kangeroo Hoodie",
  "price": 52,
  "product_type": "configurable",
  "quote_id": quote_id,
  "product_option": {
    "extension_attributes": {
      "configurable_item_options": [
        {
          "option_id": "93",
          "option_value": 52
        },
        {
          "option_id": "141",
          "option_value": 168
        }
      ]
    }
  }
}
```

### Add a bundle product to a cart

The sample data provides one bundled product, the Sprite Yoga Companion Kit (`sku`: `24-WG080`). The kit contains the following items:

*  Sprite Statis Ball in sizes 55 cm (`sku`: `24-WG081-blue`), 65 cm (`sku`: `24-WG082-blue`), or 75 cm (`sku`: `24-WG083-blue`)
*  Sprite Foam Yoga brick (`sku`: `24-WG084`)
*  Sprite Yoga Strap in lengths 6 ft (`sku`: `24-WG085`), 8 ft (`sku`: `24-WG086`), or 10 ft (`sku`: `24-WG087`)
*  Sprite Foam Roller (`sku`: `24-WG088`)

To add a bundle product to a cart, you must specify the `sku` of the bundle product, but not the individual items. You add individual items to the bundle product by specifying the `id` defined in the item's `product_links` object. The `product_links` object primarily describes the ordering and placement of options on the customization page, but it also links an item's `sku` and `id` to the `sku` of the bundle product.

The `GET <host>/rest/default/V1/bundle-products/24-WG080/options/all` call returns `id` values, as shown in the following simplified response:

```json
[
  {
    "option_id": 1,
    "title": "Sprite Stasis Ball",
    "required": true,
    "type": "radio",
    "position": 1,
    "sku": "24-WG080",
    "product_links": [
      {
        "id": "1",
        "sku": "24-WG081-blue",
        "option_id": 1,
        "qty": 1
      },
      {
        "id": "2",
        "sku": "24-WG082-blue",
        "option_id": 1,
        "qty": 1
      },
      {
        "id": "3",
        "sku": "24-WG083-blue",
        "option_id": 1,
        "qty": 1
      }
    ]
  },
  {
    "option_id": 2,
    "title": "Sprite Foam Yoga Brick",
    "required": true,
    "type": "radio",
    "position": 2,
    "sku": "24-WG080",
    "product_links": [
      {
        "id": "4",
        "sku": "24-WG084",
        "option_id": 2,
        "qty": 1
      }
    ]
  },
  {
    "option_id": 3,
    "title": "Sprite Yoga Strap",
    "required": true,
    "type": "radio",
    "position": 3,
    "sku": "24-WG080",
    "product_links": [
      {
        "id": "5",
        "sku": "24-WG085",
        "option_id": 3,
        "qty": 1
      },
      {
        "id": "6",
        "sku": "24-WG086",
        "option_id": 3,
        "qty": 1
      },
      {
        "id": "7",
        "sku": "24-WG087",
        "option_id": 3,
        "qty": 1
      }
    ]
  },
  {
    "option_id": 4,
    "title": "Sprite Foam Roller",
    "required": true,
    "type": "radio",
    "position": 4,
    "sku": "24-WG080",
    "product_links": [
      {
        "id": "8",
        "sku": "24-WG088",
        "option_id": 4,
        "qty": 1
      }
    ]
  }
]
```

For this example, we'll configure the Sprite Yoga Companion Kit as follows:

*  65 cm Sprite Stasis Ball (`id`: `2`)
*  Sprite Foam Yoga Brick (`id`: `4`)
*  8 ft Sprite Yoga strap (`id`: `6`)
*  Sprite Foam Roller (`id`: `8`)

**Endpoint:**
`POST <host>/rest/default/V1/carts/mine/items`

**Headers:**
`Content-Type: application/json`
`Authorization: Bearer <customer token>`

#### Payload

```json
{
  "cartItem": {
    "sku": "24-WG080",
    "qty": 1,
    "quote_id": quote_id,
    "product_option": {
      "extension_attributes": {
        "bundle_options": [
          {
            "option_id": 1,
            "option_qty": 1,
            "option_selections": [2]
          },
          {
            "option_id": 2,
            "option_qty": 1,
            "option_selections": [4]
          },
          {
            "option_id": 3,
            "option_qty": 1,
            "option_selections": [6]
          },
          {
            "option_id": 4,
            "option_qty": 1,
            "option_selections": [8]
          }
        ]
      }
    }
  }
}
```

#### Response

```json
{
  "item_id": 9,
  "sku": "24-WG080-24-WG084-24-WG088-24-WG082-blue-24-WG086",
  "qty": 1,
  "name": "Sprite Yoga Companion Kit",
  "price": 68,
  "product_type": "bundle",
  "quote_id": quote_id,
  "product_option": {
    "extension_attributes": {
      "bundle_options": [
        {
          "option_id": 1,
          "option_qty": 1,
          "option_selections": [
            2
          ]
        },
        {
          "option_id": 2,
          "option_qty": 1,
          "option_selections": [
            4
          ]
        },
        {
          "option_id": 3,
          "option_qty": 1,
          "option_selections": [
            6
          ]
        },
        {
          "option_id": 4,
          "option_qty": 1,
          "option_selections": [
            8
          ]
        }
      ]
    }
  }
}
```
