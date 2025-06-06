# Configcat API

## Sync overview

This source can sync data from the [Configcat API](https://api.configcat.com/docs). At present this connector only supports full refresh syncs meaning that each time you use the connector it will sync all available records from scratch. Please use cautiously if you expect your API to have a lot of records.

## This Source Supports the Following Streams

- organizations
- organization_members
- products
- tags
- environments

### Features

| Feature           | Supported?\(Yes/No\) | Notes |
| :---------------- | :------------------- | :---- |
| Full Refresh Sync | Yes                  |       |
| Incremental Sync  | No                   |       |

### Performance considerations

Configcat APIs are under rate limits for the number of API calls allowed per API keys per second. If you reach a rate limit, API will return a 429 HTTP error code. See [here](https://api.configcat.com/docs/#section/Throttling-and-rate-limits)

## Getting started

### Requirements

- Username
- Password

## Changelog

<details>
  <summary>Expand to review</summary>

| Version | Date       | Pull Request                                              | Subject                                     |
| :------ | :--------- | :-------------------------------------------------------- | :------------------------------------------ |
| 0.2.21 | 2025-04-26 | [58850](https://github.com/airbytehq/airbyte/pull/58850) | Update dependencies |
| 0.2.20 | 2025-04-19 | [58326](https://github.com/airbytehq/airbyte/pull/58326) | Update dependencies |
| 0.2.19 | 2025-04-12 | [57762](https://github.com/airbytehq/airbyte/pull/57762) | Update dependencies |
| 0.2.18 | 2025-04-05 | [57211](https://github.com/airbytehq/airbyte/pull/57211) | Update dependencies |
| 0.2.17 | 2025-03-29 | [56543](https://github.com/airbytehq/airbyte/pull/56543) | Update dependencies |
| 0.2.16 | 2025-03-22 | [55988](https://github.com/airbytehq/airbyte/pull/55988) | Update dependencies |
| 0.2.15 | 2025-03-08 | [55288](https://github.com/airbytehq/airbyte/pull/55288) | Update dependencies |
| 0.2.14 | 2025-03-01 | [54924](https://github.com/airbytehq/airbyte/pull/54924) | Update dependencies |
| 0.2.13 | 2025-02-22 | [54378](https://github.com/airbytehq/airbyte/pull/54378) | Update dependencies |
| 0.2.12 | 2025-02-15 | [53760](https://github.com/airbytehq/airbyte/pull/53760) | Update dependencies |
| 0.2.11 | 2025-02-08 | [53341](https://github.com/airbytehq/airbyte/pull/53341) | Update dependencies |
| 0.2.10 | 2025-02-01 | [52814](https://github.com/airbytehq/airbyte/pull/52814) | Update dependencies |
| 0.2.9 | 2025-01-25 | [52297](https://github.com/airbytehq/airbyte/pull/52297) | Update dependencies |
| 0.2.8 | 2025-01-18 | [51701](https://github.com/airbytehq/airbyte/pull/51701) | Update dependencies |
| 0.2.7 | 2025-01-11 | [51102](https://github.com/airbytehq/airbyte/pull/51102) | Update dependencies |
| 0.2.6 | 2024-12-28 | [50591](https://github.com/airbytehq/airbyte/pull/50591) | Update dependencies |
| 0.2.5 | 2024-12-21 | [49996](https://github.com/airbytehq/airbyte/pull/49996) | Update dependencies |
| 0.2.4 | 2024-12-14 | [49491](https://github.com/airbytehq/airbyte/pull/49491) | Update dependencies |
| 0.2.3 | 2024-12-12 | [48256](https://github.com/airbytehq/airbyte/pull/48256) | Update dependencies |
| 0.2.2 | 2024-10-28 | [47465](https://github.com/airbytehq/airbyte/pull/47465) | Update dependencies |
| 0.2.1 | 2024-10-21 | [47194](https://github.com/airbytehq/airbyte/pull/47194) | Update dependencies |
| 0.2.0 | 2024-08-23 | [44594](https://github.com/airbytehq/airbyte/pull/44594) | Refactor connector to manifest-only format |
| 0.1.13 | 2024-08-17 | [44357](https://github.com/airbytehq/airbyte/pull/44357) | Update dependencies |
| 0.1.12 | 2024-08-12 | [43870](https://github.com/airbytehq/airbyte/pull/43870) | Update dependencies |
| 0.1.11 | 2024-08-10 | [43596](https://github.com/airbytehq/airbyte/pull/43596) | Update dependencies |
| 0.1.10 | 2024-08-03 | [43272](https://github.com/airbytehq/airbyte/pull/43272) | Update dependencies |
| 0.1.9 | 2024-07-27 | [42702](https://github.com/airbytehq/airbyte/pull/42702) | Update dependencies |
| 0.1.8 | 2024-07-20 | [42329](https://github.com/airbytehq/airbyte/pull/42329) | Update dependencies |
| 0.1.7 | 2024-07-13 | [41705](https://github.com/airbytehq/airbyte/pull/41705) | Update dependencies |
| 0.1.6 | 2024-07-10 | [41450](https://github.com/airbytehq/airbyte/pull/41450) | Update dependencies |
| 0.1.5 | 2024-07-06 | [40929](https://github.com/airbytehq/airbyte/pull/40929) | Update dependencies |
| 0.1.4 | 2024-06-25 | [40442](https://github.com/airbytehq/airbyte/pull/40442) | Update dependencies |
| 0.1.3 | 2024-06-22 | [40076](https://github.com/airbytehq/airbyte/pull/40076) | Update dependencies |
| 0.1.2 | 2024-06-06 | [39230](https://github.com/airbytehq/airbyte/pull/39230) | [autopull] Upgrade base image to v1.2.2 |
| 0.1.1 | 2024-05-21 | [38547](https://github.com/airbytehq/airbyte/pull/38547) | [autopull] base image + poetry + up_to_date |
| 0.1.0   | 2022-10-30 | [#18649](https://github.com/airbytehq/airbyte/pull/18649) | 🎉 New Source: Configcat API [low-code CDK] |

</details>
