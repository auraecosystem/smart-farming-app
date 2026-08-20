> ## Documentation Index
> Fetch the complete documentation index at: https://docs.etherscan.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Daily Network Transaction Fee

> Retrieves the total transaction fees paid to miners each day.

export const chain = '1';

<Note>This is a PRO endpoint, available to the [Standard Plan](/resources/rate-limits) and above</Note>

### Query Parameters

<ParamField query="apikey" type="string" default="YourApiKeyToken">
  Your Etherscan API key.
</ParamField>

<ParamField query="chainid" type="string" default="1">
  Chain ID to query, eg `1` for Ethereum, `8453` for Base from our [supported chains](/supported-chains).
</ParamField>

<ParamField query="module" type="string" default="stats">
  Set to `stats` for this endpoint.
</ParamField>

<ParamField query="action" type="string" default="dailytxnfee">
  Set to `dailytxnfee` for this endpoint.
</ParamField>

<ParamField query="startdate" type="string" default="2019-02-01">
  Starting date in `yyyy-MM-dd` format.
</ParamField>

<ParamField query="enddate" type="string" default="2019-02-28">
  Ending date in `yyyy-MM-dd` format.
</ParamField>

<ParamField query="sort" type="string" default="asc">
  Sort order either `desc` for the latest results first or `asc` for the oldest results first.
</ParamField>

<ResponseExample>
  ```json theme={null}
  {
    "status": "1",
    "message": "OK",
    "result": [
      {
        "UTCDate": "2019-02-01",
        "unixTimeStamp": "1548979200",
        "transactionFee_Eth": "358.558440870590355682"
      },
      {
        "UTCDate": "2019-02-02",
        "unixTimeStamp": "1549065600",
        "transactionFee_Eth": "286.886084685869906669"
      }
    ]
  }
  ```
</ResponseExample>
