resource "aws_apigatewayv2_api" "movie_api" {
  name          = "movie-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_headers = ["*"]
  }
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.movie_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.movie_api.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "get_all_movies" {
  api_id    = aws_apigatewayv2_api.movie_api.id
  route_key = "GET /getmovies"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "get_movies_by_year" {
  api_id    = aws_apigatewayv2_api.movie_api.id
  route_key = "GET /getmoviesbyyear/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "get_movie_summary" {
  api_id    = aws_apigatewayv2_api.movie_api.id
  route_key = "GET /getmoviesummary/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "api_stage" {
  api_id      = aws_apigatewayv2_api.movie_api.id
  name        = var.api_stage_name
  auto_deploy = true
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.movie_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.movie_api.execution_arn}/*/*"
}

output "api_gateway_url" {
  value = aws_apigatewayv2_stage.api_stage.invoke_url
}
