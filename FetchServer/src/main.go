package main

import (
	"Responses"
	"Service"
	"flag"
)

var (
	apiKey = flag.String(
		"api_key",
		"",
		"An API key used for YT content fetching.",
	)

	maxResults = flag.Int(
		"max_results",
		10,
		"The max amount of fetched videos in a single search.",
	)

	hostname = flag.String(
		"hostname",
		"localhost",
		"The host name used for connecting to the existing API.",
	)

	port = flag.Int(
		"port",
		9998,
		"The port that allows connection to this host.",
	)
)

func main() {
	flag.Parse()

	if len(*apiKey) == 0 {
		panic("Incorrect api key.")
	}

	service := Service.New(*apiKey)
	router := Responses.New(&service)

	router.Run()
}
