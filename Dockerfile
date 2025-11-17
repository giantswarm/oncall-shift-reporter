FROM alpine:3.11

 RUN apk update && apk --no-cache add ca-certificates && \
  update-ca-certificates

 ADD ./oncall-shift-reporter /usr/local/bin/oncall-shift-reporter
ENTRYPOINT ["/usr/local/bin/oncall-shift-reporter"]
