import json
import boto3

def calculate_number_of_occurrences(event, context):
  """Calculates the number of occurrences of a character in a string.

  Args:
    event: The event object from Lambda.
    context: The context object from Lambda.

  Returns:
    A JSON object containing the number of occurrences of the character in the string.
  """

  string = event["string"]
  character = event["character"]

  dynamo_client = boto3.client("dynamodb")

  response = dynamo_client.get_item(
    TableName=context.function_name,
    Key={
      "id": {
        "S": str(uuid.uuid4())
      }
    }
  )

  if response["Item"]:
    return response["Item"]["number_of_occurrences"]

  number_of_occurrences = string.count(character)

  dynamo_client.put_item(
    TableName=context.function_name,
    Item={
      "id": {
        "S": str(uuid.uuid4())
      },
      "number_of_occurrences": {
        "N": str(number_of_occurrences)
      }
    }
  )

  return {
    "number_of_occurrences": number_of_occurrences
  }
