# ======================================
#            URLS Component
# ======================================

API_VERSION = "v1"
BASE_URL = "http://api.remix.bestbuy.com/{0}/".format(API_VERSION)

# ======================================
#    Product Search Description Types
# ======================================

PRODUCT_DESCRIPTION_TYPES = {
    1: "name",
    2: "description",
    3: "shortDescription",
    4: "longDescription"
}

PRODUCT_SEARCH_CRITERIA_TYPES = {
    1: "customerReviewAverage",
    2: "customerReviewCount"
}

# ======================================
#         Valid Search Params
# ======================================

PRODUCT_SEARCH_PARAMS = [
    "accessories.sku",
    "color",
    "condition",
    "customerReviewAverage",
    "customerReviewCount",
    "customerTopRated ",
    "depth",
    "description",
    "details.name ",
    "details.value",
    "digital",
    "features.feature ",
    "format",
    "frequentlyPurchasedWith.sku",
    "height",
    "includedItemList.includedItem",
    "longDescription",
    "longDescriptionHtml",
    "manufacturer ",
    "modelNumber",
    "name ",
    "preowned ",
    "quantityLimit",
    "relatedProducts.sku",
    "releaseDate",
    "shortDescription ",
    "shortDescriptionHtml ",
    "sku",
    "upc",
    "warrantyLabor",
    "warrantyParts",
    "weight",
    "width"
]
