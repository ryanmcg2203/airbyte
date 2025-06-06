#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#
import json
import math
from unittest.mock import MagicMock, patch

import pytest
import requests
from source_shopify.auth import ShopifyAuthenticator
from source_shopify.source import ConnectionCheckTest, ShopifyScopes, SourceShopify
from source_shopify.streams.streams import (
    AbandonedCheckouts,
    Articles,
    Blogs,
    Collects,
    Countries,
    CustomCollections,
    Customers,
    DiscountCodes,
    DraftOrders,
    FulfillmentOrders,
    Fulfillments,
    InventoryLevels,
    Locations,
    MetafieldArticles,
    MetafieldBlogs,
    MetafieldCollections,
    MetafieldCustomers,
    MetafieldDraftOrders,
    MetafieldLocations,
    MetafieldOrders,
    MetafieldPages,
    MetafieldProducts,
    MetafieldProductVariants,
    MetafieldShops,
    MetafieldSmartCollections,
    OrderRefunds,
    OrderRisks,
    Orders,
    Pages,
    PriceRules,
    ProductImages,
    Products,
    ProductVariants,
    Shop,
    TenderTransactions,
    Transactions,
    TransactionsGraphql,
)

from airbyte_cdk.utils import AirbyteTracedException

from .conftest import records_per_slice


@pytest.fixture
def config(basic_config) -> dict:
    basic_config["start_date"] = "2020-11-01"
    basic_config["authenticator"] = ShopifyAuthenticator(basic_config)
    return basic_config


@pytest.mark.parametrize(
    "stream,stream_slice,expected_path",
    [
        (Articles, None, "articles.json"),
        (Blogs, None, "blogs.json"),
        (MetafieldBlogs, {"id": 123}, "blogs/123/metafields.json"),
        (MetafieldArticles, {"id": 123}, "articles/123/metafields.json"),
        # GraphQL Bulk Streams
        (MetafieldCustomers, None, "graphql.json"),
        (MetafieldOrders, None, "graphql.json"),
        (MetafieldDraftOrders, None, "graphql.json"),
        (MetafieldProducts, None, "graphql.json"),
        (MetafieldProductVariants, None, "graphql.json"),
        (MetafieldLocations, None, "graphql.json"),
        (MetafieldCollections, None, "graphql.json"),
        (Products, None, "graphql.json"),
        (ProductImages, None, "graphql.json"),
        (ProductVariants, None, "graphql.json"),
        # Nested Substreams
        (OrderRefunds, None, ""),
        # regular streams
        (MetafieldSmartCollections, {"id": 123}, "smart_collections/123/metafields.json"),
        (MetafieldPages, {"id": 123}, "pages/123/metafields.json"),
        (MetafieldShops, None, "metafields.json"),
        (Customers, None, "customers.json"),
        (Orders, None, "orders.json"),
        (DraftOrders, None, "draft_orders.json"),
        (AbandonedCheckouts, None, "checkouts.json"),
        (Collects, None, "collects.json"),
        (TenderTransactions, None, "tender_transactions.json"),
        (Pages, None, "pages.json"),
        (PriceRules, None, "price_rules.json"),
        (Locations, None, "locations.json"),
        (Shop, None, "shop.json"),
        (CustomCollections, None, "custom_collections.json"),
    ],
)
def test_path(stream, stream_slice, expected_path, config) -> None:
    stream = stream(config)
    if stream_slice:
        result = stream.path(stream_slice)
    else:
        result = stream.path()
    assert result == expected_path


@pytest.mark.parametrize(
    "stream,stream_slice,expected_path",
    [
        (Transactions, {"order_id": 12345}, "orders/12345/transactions.json"),
        # Nested Substreams
        (OrderRefunds, None, ""),
        (Fulfillments, None, ""),
        # GQL BULK stream
        (OrderRisks, None, "graphql.json"),
        (DiscountCodes, None, "graphql.json"),
        (FulfillmentOrders, None, "graphql.json"),
        (InventoryLevels, None, "graphql.json"),
    ],
)
def test_path_with_stream_slice_param(stream, stream_slice, expected_path, config) -> None:
    stream = stream(config)
    if stream_slice:
        result = stream.path(stream_slice)
    else:
        result = stream.path()
    assert result == expected_path


@pytest.mark.parametrize(
    "stream, parent_records, state_checkpoint_interval",
    [
        (
            OrderRefunds,
            [
                {"id": 1, "refunds": [{"created_at": "2021-01-01T00:00:00+00:00"}]},
                {"id": 2, "refunds": [{"created_at": "2021-02-01T00:00:00+00:00"}]},
                {"id": 3, "refunds": [{"created_at": "2021-03-01T00:00:00+00:00"}]},
                {"id": 4, "refunds": [{"created_at": "2021-04-01T00:00:00+00:00"}]},
                {"id": 5, "refunds": [{"created_at": "2021-05-01T00:00:00+00:00"}]},
            ],
            2,
        ),
    ],
)
def test_stream_slice_nested_substream_buffering(
    mocker,
    config,
    stream,
    parent_records,
    state_checkpoint_interval,
) -> None:
    # making the stream instance
    stream = stream(config)
    stream.state_checkpoint_interval = state_checkpoint_interval
    # simulating `read_records` for the `parent_stream`
    mocker.patch(
        "source_shopify.streams.base_streams.IncrementalShopifyStreamWithDeletedEvents.read_records",
        return_value=parent_records,
    )
    # count how many slices we expect, based on the number of parent_records
    total_slices_expected = math.ceil(len(parent_records) / state_checkpoint_interval)
    # define the how many records each individual slice should have, based on the number of parent_records
    expected_records_per_slice = records_per_slice(parent_records, state_checkpoint_interval)
    # slices counter
    total_slices: int = 0
    for slice in enumerate(stream.stream_slices()):
        slice_index = slice[0]
        nested_records = slice[1].get(stream.nested_entity)
        # check the number of records / slice
        assert len(nested_records) == expected_records_per_slice[slice_index]
        # count total slices
        total_slices += 1
    # check we have emitted complete number of slices
    assert total_slices == total_slices_expected


def test_check_connection(config, mocker) -> None:
    mocker.patch("source_shopify.streams.streams.Shop.read_records", return_value=[{"id": 1}])
    source = SourceShopify()
    logger_mock = MagicMock()
    assert source.check_connection(logger_mock, config) == (True, None)


def test_read_records(config, mocker) -> None:
    records = [{"created_at": "2022-10-10T06:21:53-07:00", "orders": {"updated_at": "2022-10-10T06:21:53-07:00"}}]
    stream_slice = records[0]
    stream = OrderRefunds(config)
    mocker.patch("source_shopify.streams.base_streams.IncrementalShopifyNestedStream.read_records", return_value=records)
    assert stream.read_records(stream_slice=stream_slice)[0] == records[0]


@pytest.mark.parametrize(
    "stream, expected",
    [
        # Nested Substream
        (OrderRefunds, {}),
        #
        (Orders, {"limit": 250, "status": "any", "order": "updated_at asc", "updated_at_min": "2020-11-01"}),
        (
            AbandonedCheckouts,
            {"limit": 250, "status": "any", "order": "updated_at asc", "updated_at_min": "2020-11-01"},
        ),
    ],
)
def test_request_params(config, stream, expected) -> None:
    assert stream(config).request_params() == expected


@pytest.mark.parametrize(
    "last_record, current_state, expected",
    [
        # no init state
        (
            {"created_at": "2022-10-10T06:21:53-07:00"},
            {},
            {"created_at": "2022-10-10T06:21:53-07:00", "orders": {"updated_at": "", "deleted": {"deleted_at": ""}}},
        ),
        # state is empty str
        (
            {"created_at": "2022-10-10T06:21:53-07:00"},
            {"created_at": ""},
            {"created_at": "2022-10-10T06:21:53-07:00", "orders": {"updated_at": "", "deleted": {"deleted_at": ""}}},
        ),
        # state is None
        (
            {"created_at": "2022-10-10T06:21:53-07:00"},
            {"created_at": None},
            {"created_at": "2022-10-10T06:21:53-07:00", "orders": {"updated_at": "", "deleted": {"deleted_at": ""}}},
        ),
        # last rec cursor is None
        ({"created_at": None}, {"created_at": None}, {"created_at": "", "orders": {"updated_at": "", "deleted": {"deleted_at": ""}}}),
        # last rec cursor is empty str
        ({"created_at": ""}, {"created_at": "null"}, {"created_at": "null", "orders": {"updated_at": "", "deleted": {"deleted_at": ""}}}),
        # no values at all
        ({}, {}, {"created_at": "", "orders": {"updated_at": "", "deleted": {"deleted_at": ""}}}),
    ],
    ids=[
        "no init state",
        "state is empty str",
        "state is None",
        "last rec cursor is None",
        "last rec cursor is empty str",
        "no values at all",
    ],
)
def test_get_updated_state(config, last_record, current_state, expected) -> None:
    stream = OrderRefunds(config)
    assert stream.get_updated_state(current_state, last_record) == expected


def test_parse_response_with_bad_json(config, response_with_bad_json) -> None:
    stream = Customers(config)
    assert list(stream.parse_response(response_with_bad_json)) == [{}]


@pytest.mark.parametrize(
    "shop, expected",
    [
        ("test-store", "test-store"),
        ("test-store.myshopify.com", "test-store"),
    ],
    ids=["old style", "oauth style"],
)
def test_get_shop_name(config, shop, expected) -> None:
    source = SourceShopify()
    config["shop"] = shop
    actual = source.get_shop_name(config)
    assert actual == expected


@pytest.mark.parametrize(
    "config, expected_stream_class",
    [
        ({"fetch_transactions_user_id": False}, TransactionsGraphql),
        ({"fetch_transactions_user_id": True}, Transactions),
        ({}, TransactionsGraphql),
    ],
    ids=["don't fetch user_id", "fetch user id", "unset config value shouldn't fetch user_id"],
)
def test_select_transactions_stream(config, expected_stream_class):
    config["shop"] = "test-store"
    config["credentials"] = {"auth_method": "api_password", "api_password": "shppa_123"}
    config["authenticator"] = ShopifyAuthenticator(config)

    source = SourceShopify()
    actual = source.select_transactions_stream(config)
    assert type(actual) == expected_stream_class


@pytest.mark.parametrize(
    "read_records, expected_shop_id, expected_error",
    [
        pytest.param([{"id": "12345"}], "12345", None, id="test_shop_name_exists"),
        pytest.param([], None, AirbyteTracedException, id="test_shop_name_does_not_exist"),
    ],
)
def test_get_shop_id(config, read_records, expected_shop_id, expected_error):
    check_test = ConnectionCheckTest(config)

    with patch.object(Shop, "read_records", return_value=read_records):
        if expected_error:
            with pytest.raises(expected_error):
                check_test.get_shop_id()
        else:
            actual_shop_id = check_test.get_shop_id()
            assert actual_shop_id == expected_shop_id


def test_test_connection(config):
    config.pop("shop", None)
    check_test = ConnectionCheckTest(config)
    expected = (False, "The `Shopify Store` name is missing. Make sure it's entered and valid.")
    assert check_test.test_connection() == expected


def test_format_stream_name() -> None:
    source = SourceShopify()
    assert source.format_stream_name("test_stream") == "TestStream"


def test_user_scopes_generate_full_list_of_streams(config, mocker):
    source = SourceShopify()

    # the list of the scopes we expect user to have
    expected_user_scopes = [
        "read_customers",
        "read_orders",
        "read_draft_orders",
        "read_products",
        "read_inventory",
        "read_publications",
        "read_content",
        "read_price_rules",
        "read_discounts",
        "read_locations",
        "read_inventory",
        "read_merchant_managed_fulfillment_orders",
        "read_shipping",
        "read_shopify_payments_payouts",
        "read_online_store_pages",
    ]

    # patch the output for the critical methods
    mocker.patch.object(ShopifyAuthenticator, "get_auth_header", return_value={"X-Shopify-Access-Token": "test_toke"})
    mocker.patch.object(ConnectionCheckTest, "get_shop_id", return_value=123456)
    mocker.patch.object(ShopifyScopes, "get_user_scopes", return_value=expected_user_scopes)

    # Adjust this number based on the actual permitted streams
    expected_streams_number = 45
    assert len(source.streams(config)) == expected_streams_number


@pytest.mark.parametrize(
    "response_data, expected_token",
    [
        # Case 1: Empty page (no nodes, no next page)
        (
            {
                "data": {
                    "deliveryProfiles": {
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                        "nodes": [],
                    }
                }
            },
            None,
        ),
        # Case 2: Parent page iteration (parent page has next page, sub-page does not)
        (
            {
                "data": {
                    "deliveryProfiles": {
                        "pageInfo": {"hasNextPage": True, "endCursor": "parent_cursor"},
                        "nodes": [
                            {
                                "profileLocationGroups": [
                                    {
                                        "locationGroupZones": {
                                            "nodes": [],
                                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                                        }
                                    }
                                ]
                            }
                        ],
                    }
                }
            },
            {"cursor": "parent_cursor", "sub_cursor": None},
        ),
        # Case 3: Sub-page iteration (sub-page has next page regardless of parent page)
        (
            {
                "data": {
                    "deliveryProfiles": {
                        "pageInfo": {"hasNextPage": False, "endCursor": "parent_cursor"},
                        "nodes": [
                            {
                                "profileLocationGroups": [
                                    {
                                        "locationGroupZones": {
                                            "nodes": [],
                                            "pageInfo": {"hasNextPage": True, "endCursor": "sub_cursor"},
                                        }
                                    }
                                ]
                            }
                        ],
                    }
                }
            },
            {"cursor": None, "sub_cursor": "sub_cursor"},
        ),
    ],
)
def test_countries_next_page_token(config, response_data, expected_token):
    config["shop"] = "test-store"
    config["credentials"] = {"auth_method": "api_password", "api_password": "shppa_123"}
    config["authenticator"] = ShopifyAuthenticator(config)

    # Instantiate the Countries stream with a dummy config.
    stream = Countries(config=config, parent=None)

    response_body = json.dumps(response_data)
    response = requests.Response()
    response.status_code = 200
    response._content = response_body.encode("utf-8")

    token = stream.next_page_token(response)
    assert token == expected_token


def test_countries_process_country(config, countries_record_data, countries_expected_record_data):
    config["credentials"] = {"auth_method": "api_password", "api_password": "shppa_123"}
    config["authenticator"] = ShopifyAuthenticator(config)

    # Instantiate the Countries stream with a dummy config.
    stream = Countries(config=config, parent=None)
    assert stream._process_country(countries_record_data) == countries_expected_record_data


def test_countries_request_body_json(config):
    config["shop"] = "test-store"
    config["credentials"] = {"auth_method": "api_password", "api_password": "shppa_123"}
    config["authenticator"] = ShopifyAuthenticator(config)

    # Instantiate the Countries stream with a dummy config.
    stream = Countries(config=config, parent=None)
    stream_slice = {"parent": {"profile_location_groups": [{"locationGroup": {"id": "location/group/id"}}]}}
    request_body = stream.request_body_json(stream_slice=stream_slice, stream_state={})

    expected_request_body = {
        "query": """query DeliveryZoneList {
  deliveryProfiles(
    first: 1
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      profileLocationGroups(
        locationGroupId: "location/group/id"
      ) {
        locationGroupZones(
          first: 100
        ) {
          nodes {
            zone {
              id
              name
              countries {
                id
                name
                translated_name: translatedName
                code {
                  country_code: countryCode
                  rest_of_world: restOfWorld
                }
                provinces {
                  id
                  name
                  code
                  translated_name: translatedName
                }
              }
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
  }
}"""
    }
    assert request_body == expected_request_body


def test_countries_parse_response(config, countries_response_data, countries_expected_record_data):
    config["credentials"] = {"auth_method": "api_password", "api_password": "shppa_123"}
    config["authenticator"] = ShopifyAuthenticator(config)

    # Instantiate the Countries stream with a dummy config.
    stream = Countries(config=config, parent=None)
    response = MagicMock(status_code=requests.codes.OK)
    response.json.return_value = countries_response_data

    records = stream.parse_response(response)
    expected_records = [
        countries_expected_record_data,
    ]
    assert list(records) == expected_records
