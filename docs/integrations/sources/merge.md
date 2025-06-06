# Merge

This page contains the setup guide and reference information for the [Merge](https://docs.merge.dev/ats/overview/) source

## Prerequisites

Access Token (which acts as bearer token) and linked accounts tokens are mandate for this connector to work, It could be seen at settings (Bearer ref - https://app.merge.dev/keys) and (Account token ref - https://app.merge.dev/keys).

## Setup guide

### Step 1: Set up Merge connection

- Link your other integrations with account credentials on accounts section (ref - https://app.merge.dev/linked-accounts/accounts)
- Get your bearer token on keys section (ref - https://app.merge.dev/keys)
- Setup params (All params are required)
- Available params
  - account_token: Linked account token seen after integration at linked account section
  - api_token: Bearer token seen at keys section, try to use production keys
  - start_date: Date filter for eligible streams

## Step 2: Set up the Merge connector in Airbyte

### For Airbyte Cloud:

1. [Log into your Airbyte Cloud](https://cloud.airbyte.io/workspaces) account.
2. In the left navigation bar, click **Sources**. In the top-right corner, click **+new source**.
3. On the Set up the source page, enter the name for the merge connector and select **Merge** from the Source type dropdown.
4. Enter your `account_token, api_token and start_date`.
5. Click **Set up source**.

### For Airbyte OSS:

1. Navigate to the Airbyte Open Source dashboard.
2. Set the name for your source.
3. Enter your `account_token, api_token and start_date`.
4. Click **Set up source**.

## Supported sync modes

The Merge source connector supports the following [sync modes](https://docs.airbyte.com/cloud/core-concepts#connection-sync-modes):

| Feature                       | Supported? |
| :---------------------------- | :--------- |
| Full Refresh Sync             | Yes        |
| Incremental Sync              | No         |
| Replicate Incremental Deletes | No         |
| SSL connection                | Yes        |
| Namespaces                    | No         |

## Supported Streams

- account_details
- activities
- applications
- attachments
- candidates
- departments
- eeocs
- interviews
- job-interview-stages
- jobs
- offers
- offices
- sync_status
- users

## API method example

GET https://api.merge.dev/api/ats/v1/account-details

## Performance considerations

Merge [API reference](https://api.merge.dev/api/ats/v1/) has v1 at present. The connector as default uses v1.

## Changelog

<details>
  <summary>Expand to review</summary>

| Version | Date       | Pull Request                                       | Subject        |
| :------ | :--------- | :------------------------------------------------- | :------------- |
| 0.2.21 | 2025-04-26 | [58819](https://github.com/airbytehq/airbyte/pull/58819) | Update dependencies |
| 0.2.20 | 2025-04-19 | [58225](https://github.com/airbytehq/airbyte/pull/58225) | Update dependencies |
| 0.2.19 | 2025-04-12 | [57679](https://github.com/airbytehq/airbyte/pull/57679) | Update dependencies |
| 0.2.18 | 2025-04-05 | [57085](https://github.com/airbytehq/airbyte/pull/57085) | Update dependencies |
| 0.2.17 | 2025-03-29 | [56706](https://github.com/airbytehq/airbyte/pull/56706) | Update dependencies |
| 0.2.16 | 2025-03-22 | [56049](https://github.com/airbytehq/airbyte/pull/56049) | Update dependencies |
| 0.2.15 | 2025-03-08 | [55468](https://github.com/airbytehq/airbyte/pull/55468) | Update dependencies |
| 0.2.14 | 2025-03-01 | [54825](https://github.com/airbytehq/airbyte/pull/54825) | Update dependencies |
| 0.2.13 | 2025-02-22 | [54301](https://github.com/airbytehq/airbyte/pull/54301) | Update dependencies |
| 0.2.12 | 2025-02-15 | [53802](https://github.com/airbytehq/airbyte/pull/53802) | Update dependencies |
| 0.2.11 | 2025-02-08 | [53274](https://github.com/airbytehq/airbyte/pull/53274) | Update dependencies |
| 0.2.10 | 2025-02-01 | [52715](https://github.com/airbytehq/airbyte/pull/52715) | Update dependencies |
| 0.2.9 | 2025-01-25 | [52234](https://github.com/airbytehq/airbyte/pull/52234) | Update dependencies |
| 0.2.8 | 2025-01-18 | [51822](https://github.com/airbytehq/airbyte/pull/51822) | Update dependencies |
| 0.2.7 | 2025-01-11 | [51221](https://github.com/airbytehq/airbyte/pull/51221) | Update dependencies |
| 0.2.6 | 2024-12-28 | [50627](https://github.com/airbytehq/airbyte/pull/50627) | Update dependencies |
| 0.2.5 | 2024-12-21 | [50092](https://github.com/airbytehq/airbyte/pull/50092) | Update dependencies |
| 0.2.4 | 2024-12-14 | [49652](https://github.com/airbytehq/airbyte/pull/49652) | Update dependencies |
| 0.2.3 | 2024-12-12 | [49222](https://github.com/airbytehq/airbyte/pull/49222) | Update dependencies |
| 0.2.2 | 2024-12-11 | [47906](https://github.com/airbytehq/airbyte/pull/47906) | Starting with this version, the Docker image is now rootless. Please note that this and future versions will not be compatible with Airbyte versions earlier than 0.64 |
| 0.2.1 | 2024-10-28 | [47593](https://github.com/airbytehq/airbyte/pull/47593) | Update dependencies |
| 0.2.0 | 2024-08-26 | [44768](https://github.com/airbytehq/airbyte/pull/44768) | Refactor connector to manifest-only format |
| 0.1.15 | 2024-08-24 | [44665](https://github.com/airbytehq/airbyte/pull/44665) | Update dependencies |
| 0.1.14 | 2024-08-17 | [44297](https://github.com/airbytehq/airbyte/pull/44297) | Update dependencies |
| 0.1.13 | 2024-08-12 | [43778](https://github.com/airbytehq/airbyte/pull/43778) | Update dependencies |
| 0.1.12 | 2024-08-10 | [43661](https://github.com/airbytehq/airbyte/pull/43661) | Update dependencies |
| 0.1.11 | 2024-08-03 | [43074](https://github.com/airbytehq/airbyte/pull/43074) | Update dependencies |
| 0.1.10 | 2024-07-27 | [42645](https://github.com/airbytehq/airbyte/pull/42645) | Update dependencies |
| 0.1.9 | 2024-07-20 | [42313](https://github.com/airbytehq/airbyte/pull/42313) | Update dependencies |
| 0.1.8 | 2024-07-13 | [41862](https://github.com/airbytehq/airbyte/pull/41862) | Update dependencies |
| 0.1.7 | 2024-07-10 | [41572](https://github.com/airbytehq/airbyte/pull/41572) | Update dependencies |
| 0.1.6 | 2024-07-09 | [41246](https://github.com/airbytehq/airbyte/pull/41246) | Update dependencies |
| 0.1.5 | 2024-07-06 | [40932](https://github.com/airbytehq/airbyte/pull/40932) | Update dependencies |
| 0.1.4 | 2024-06-25 | [40272](https://github.com/airbytehq/airbyte/pull/40272) | Update dependencies |
| 0.1.3 | 2024-06-22 | [40163](https://github.com/airbytehq/airbyte/pull/40163) | Update dependencies |
| 0.1.2 | 2024-06-06 | [39238](https://github.com/airbytehq/airbyte/pull/39238) | [autopull] Upgrade base image to v1.2.2 |
| 0.1.1 | 2024-05-20 | [38445](https://github.com/airbytehq/airbyte/pull/38445) | [autopull] base image + poetry + up_to_date |
| 0.1.0   | 2023-04-18 | [Init](https://github.com/airbytehq/airbyte/pull/) | Initial commit |

</details>
