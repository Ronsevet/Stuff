import json
import boto3

def get_number_of_occurrences(event, context):
  """Gets the number of occurrences of a character in a string, given the unique identifier.

  Args:
    event: The event object from Lambda.
    context: The context object from Lambda.

  Returns:
    A JSON object containing the number of occurrences of the character in the string.
  """

  unique_identifier = event["unique_identifier"]

  dynamo_client = boto3.client("dynamodb")

  response = dynamo_client.get_item(
    TableName=context.function_name,
    Key={
      "id": {
        "S": unique_identifier
      }
    }
  )

  if response["Item"]:
    return response["Item"]["number_of_occurrences"]

  return {
    "error": "The unique identifier is not valid."
  }
