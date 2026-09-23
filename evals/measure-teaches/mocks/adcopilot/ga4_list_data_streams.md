---
type: fixed
# One web data stream on the fictional property, already carrying a
# measurement ID. Key names follow the Analytics Admin API's data stream in
# the snake_case the connector's other Analytics answers use; every value is
# invented and the measurement ID is not a real one.
---
{
  "property": "{{input.property}}",
  "data_streams": [
    {
      "name": "properties/987654321/dataStreams/5566778899",
      "type": "WEB_DATA_STREAM",
      "display_name": "Example Bakery website",
      "web_stream_data": {
        "measurement_id": "G-EXAMPLE001",
        "default_uri": "https://www.example-bakery.invalid"
      },
      "create_time": "2026-09-20T14:02:11Z"
    }
  ]
}
