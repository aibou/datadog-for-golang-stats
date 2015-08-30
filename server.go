package main

import (
    "net/http"
    "log"
    "github.com/fukata/golang-stats-api-handler"
)
func main() {
    http.HandleFunc("/api/stats", stats_api.Handler)
    log.Fatal( http.ListenAndServe(":8080", nil) )
}
