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

API_SEARCH_PARAMS = [
    "facet",
    "format",
    "show",
    "sort",
    "page",
    "pageSize"
]

PRODUCT_SEARCH_PARAMS = [
    "accessories.sku",
    "active",
    "activeUpdateDate",
    "bestBuyItemId",
    "bestSellingRank",
    "bundledin.sku",
    "collection",
    "color",
    "dollarSavings",
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
    "manufacturer ",
    "marketplace",
    "members.sku",
    "modelNumber",
    "name ",
    "new",
    "onlineAvailability",
    "onlineAvailabilityText",
    "onlineAvailabilityTextHtml",
    "onlineAvailabilityUpdateDate",
    "orderable",
    "onSale",
    "percentSavings",
    "preowned ",
    "priceRestriction",
    "priceUpdateDate",
    "priceWithPlan.newTwoYearPlan",
    "priceWithPlan.upgradeTwoYearPlan",
    "priceWithPlan.newTwoYearPlanSalePrice",
    "priceWithPlan.upgradeTwoYearPlanSalePrice",
    "priceWithPlan.newTwoYearPlanRegularPrice",
    "priceWithPlan.upgradeTwoYearPlanRegularPrice",
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
    "secondaryMarkey"
    "sellerId",
    "shipping.ground",
    "shipping.nextDay",
    "shipping.secondDay",
    "shipping.vendorDelivery",
    "shippingCost",
    "shippingWeight",
    "shortDescription ",
    "shortDescriptionHtml ",
    "source",
    "specialOrder",
    "startDate",
    "tradeInValue",
    "type",
    "upc",
    "warrantyLabor",
    "warrantyParts",
    "weight",
    "width"
]
