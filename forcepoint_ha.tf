terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.75"
    }
  }

  provider aws {
    region = var.region
  }

  module lambdas {
    source = "./lambdas"

    function_calculate_number_of_occurrences {
      handler = "calculate_number_of_occurrences.handler"
      runtime = "python3.8"
      environment {
        DYNAMODB_TABLE_NAME = var.dynamodb_table_name
      }
    }

    function_get_number_of_occurrences {
      handler = "get_number_of_occurrences.handler"
      runtime = "python3.8"
      environment {
        DYNAMODB_TABLE_NAME = var.dynamodb_table_name
      }
    }
  }

  resource api_gateway_rest_api {
    name = "duplicate-file-finder"

    endpoint_configuration {
      types = ["REGIONAL"]
    }

    resources {
      calculate_number_of_occurrences {
        path = "/calculate-number-of-occurrences"
        method = "POST"
      }

      get_number_of_occurrences {
        path = "/get-number-of-occurrences"
        method = "GET"
      }
    }

    depends_on = [
      module.lambdas.function_calculate_number_of_occurrences,
      module.lambdas.function_get_number_of_occurrences,
    ]
  }

  resource dynamodb_table {
    name = var.dynamodb_table_name

    attribute {
      name = "id"
      type = "S"
    }

    key_schema {
      attribute_name = "id"
      key_type = "HASH"
    }

    provisioned_throughput {
      read_capacity_units = 10
      write_capacity_units = 10
    }
  }
}
