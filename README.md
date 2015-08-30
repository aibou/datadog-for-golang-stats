https://github.com/fukata/golang-stats-api-handler のメトリックをdatadogに送るカスタムチェックスクリプトです。

## Run go-server and fetch metrics

    go get github.com/fukata/golang-stats-api-handler
    go run server.go

## Put the additinal check script on your datadog directory

If you use OSX, you need to put script to:

    /opt/datadog-agent/etc/checks.d/

