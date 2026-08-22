# ======================================
#            URLS Component
# ======================================

API_VERSION = "v1"
BASE_URL = f"https://api.bestbuy.com/{API_VERSION}/"
BETA_BASE_URL = "https://api.bestbuy.com/beta/"

# ======================================
#             API Names
# ======================================

PRODUCT_API = "products"
CATEGORY_API = "categories"
BULK_API = "bulk"
STORES_API = "stores"
RECOMMENDATIONS_API = "recommendations"
OPEN_BOX_API = "openBox"

# ======================================
#    Product Search Description Types
# ======================================

PRODUCT_DESCRIPTION_TYPES = {
    1: "name",
    2: "description",
    3: "shortDescription",
    4: "longDescription",
}

PRODUCT_SEARCH_CRITERIA_TYPES = {1: "customerReviewAverage", 2: "customerReviewCount"}

# ======================================
#         Valid Search Params
# ======================================

API_SEARCH_PARAMS = [
    "apiKey",
    "cursorMark",
    "facet",
    "format",
    "page",
    "pageSize",
    "show",
    "sort",
]

PRODUCT_SEARCH_PARAMS = [
    "accessories.sku",
    "active",
    "activeUpdateDate",
    "bestBuyItemId",
    "bestSellingRank",
    "bundledin.sku",
    "categoryPath.id",
    "categoryPath.name",
    "collection",
    "color",
    "condition",
    "customerReviewAverage",
    "customerReviewCount",
    "customerTopRated",
    "depth",
    "description",
    "details.name",
    "details.value",
    "digital",
    "dollarSavings",
    "features.feature",
    "format",
    "freeShipping",
    "frequentlyPurchasedWith.sku",
    "friendsAndFamilyPickup",
    "height",
    "homeDelivery",
    "includedItemList.includedItem",
    "inStoreAvailability",
    "inStoreAvailabilityText",
    "inStoreAvailabilityTextHtml",
    "inStoreAvailabilityUpdateDate",
    "inStorePickup",
    "itemUpdateDate",
    "listingId",
    "longDescription",
    "longDescriptionHtml",
    "lowPriceGuarantee",
    "manufacturer",
    "marketplace",
    "members.sku",
    "modelNumber",
    "name",
    "new",
    "onSale",
    "onlineAvailability",
    "onlineAvailabilityText",
    "onlineAvailabilityTextHtml",
    "onlineAvailabilityUpdateDate",
    "orderable",
    "percentSavings",
    "preowned",
    "priceRestriction",
    "priceUpdateDate",
    "priceWithPlan.newTwoYearPlan",
    "priceWithPlan.newTwoYearPlanRegularPrice",
    "priceWithPlan.newTwoYearPlanSalePrice",
    "priceWithPlan.upgradeTwoYearPlan",
    "priceWithPlan.upgradeTwoYearPlanRegularPrice",
    "priceWithPlan.upgradeTwoYearPlanSalePrice",
    "productId",
    "productTemple",
    "quantityLimit",
    "regularPrice",
    "relatedProducts.sku",
    "releaseDate",
    "salePrice",
    "salesRankLongTerm",
    "salesRankMediumTerm",
    "salesRankShortTerm",
    "secondaryMarket",
    "sellerId",
    "shipping.ground",
    "shipping.nextDay",
    "shipping.secondDay",
    "shipping.vendorDelivery",
    "shippingCost",
    "shippingWeight",
    "shortDescription",
    "shortDescriptionHtml",
    "source",
    "specialOrder",
    "startDate",
    "tradeInValue",
    "type",
    "upc",
    "warrantyLabor",
    "warrantyParts",
    "weight",
    "width",
]


STORE_SEARCH_PARAMS = [
    "Attribute",
    "address",
    "address2",
    "city",
    "country",
    "detailedHours",
    "distance",
    "fullPostalCode",
    "hours",
    "hoursAmPm",
    "lat",
    "lng",
    "location",
    "locationType",
    "longName",
    "name",
    "phone",
    "postalCode",
    "region",
    "services",
    "services.service",
    "storeId",
    "storeType",
]

ALL_VALID_PARAMS = set(API_SEARCH_PARAMS + PRODUCT_SEARCH_PARAMS + STORE_SEARCH_PARAMS)
