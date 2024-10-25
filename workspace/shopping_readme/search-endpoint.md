# Search for products with the /search endpoint

There are two endpoints for searching products:

*  `GET V1/search`
*  `GET V1/products`

The `GET V1/search` endpoint replicates the search capabilities that customers and guests use to find products on the storefront. The `GET V1/products` endpoint returns results an administrator would receive.

The following table highlights the differences between these two endpoints:

Property | V1/products | V1/search
--- | --- | ---
Has direct access to product data? | Yes | No (the Search engine acts as proxy)
Can specify any product attribute? | Yes | No
Contains product data in the response? | Yes | No
Are results sorted by search relevance? | No | Yes
Contains aggregations/buckets in the response? | No | Yes, for `quick_search_container` and `catalog_view_container` searches

The `V1/search` endpoint is generally more useful when you have only human (or human-like) search terms at hand, targeted to isolate a single product or a limited set of products. An added benefit is that the results are pre-sorted by their applicable search relevance.

In all other cases, for example when building and filtering product collections, and especially when other non-human backend data is available, such as an attribute's option IDs, the `V1/products` endpoint is a good choice.

## Build queries for V1/search

The basic structure of a REST call using `V1/search` follows:

```http
GET <host>/rest/default/V1/search?searchCriteria[requestName]=<container_name>&
searchCriteria[filterGroups][0][filters][0][field]=<filter_name>&
searchCriteria[filterGroups][0][filters][0][value]=<search_value>
```

By default, the container name can be one of these values:

*  quick_search_container
*  advanced_search_container
*  catalog_view_container

The possible values for the filter name and the search value are specific for each container.

Each searchable attribute defines a search boost value, which defaults to 1. However, some predefined attributes have higher values. For example, the default boost value for `sku` is 6, while the `name` has a default value of 5.

### Quick searches

The `quick_search_container` request allows you to perform the same search that a customer performs on the storefront.

By default, a filter name can be one of these:

*  `category_ids`
*  `price.from`
*  `price.to`
*  `search_term`
*  `visibility`

Quick searches return aggreggations and buckets.

#### Example

The following example performs a quick search for `digital watch`:

```http
GET <host>/rest/default/V1/search?searchCriteria[requestName]=quick_search_container&
searchCriteria[filterGroups][0][filters][0][field]=search_term&
searchCriteria[filterGroups][0][filters][0][value]=digital watch
```

### Advanced searches

The `advanced_search_container` request performs more complex searches, like those possible on the Advanced Search page.

The default filters for advanced searches can use the following [field] value:

*  `category_ids`
*  `price.from`
*  `price.to`
*  `sku`

Advanced searches can use any condition type to make comparisions, such as `like`, `eq`, or `finset`.

#### Examples

The following example get products within a price range:

```http
GET <host>/rest/default/V1/search?searchCriteria[requestName]=advanced_search_container&
searchCriteria[filterGroups][0][filters][0][field]=price.from&
searchCriteria[filterGroups][0][filters][0][value]=2&
searchCriteria[filterGroups][0][filters][1][field]=price.to&
searchCriteria[filterGroups][0][filters][1][value]=3
```

The following example gets products where the SKU might contain a specified string:

```http
GET <host>/rest/default/V1/search?searchCriteria[requestName]=advanced_search_container&
searchCriteria[filterGroups][0][filters][0][field]=sku&
searchCriteria[filterGroups][0][filters][0][value]=shirt&
searchCriteria[filterGroups][0][filters][0][condition_type]=like
```

### Catalog view searches

The `catalog_view_container`request accepts the following filters:

*  `category_ids`
*  `price.from`
*  `price.to`
*  `visibility`

Quick searches return aggreggations and buckets.

#### Example

The following example gets all products in a given category:

```http
GET <host>/rest/default/V1/search?searchCriteria[requestName]=catalog_view_container&
searchCriteria[filterGroups][0][filters][0][field]=category_ids&
searchCriteria[filterGroups][0][filters][0][value][0]=4&
searchCriteria[filterGroups][0][filters][0][condition_type]=eq
```

## Build queries for V1/products

[Search using REST](/rest/use-rest/performing-searches/) provides examples that can be used to search for products.
