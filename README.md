# apostilla-slack
Script that allows you to send message to slack channel if page is up.

Originally created to check if the page to requests apostillas in Venezuela is up, but can be configured to check other
sites.

## Arguments

-c, --channel, Channel where the message will be posted. Default: \#apostilla.

-u, --url, URL to check. Default: citaslegalizaciones.mppre.gob.ve.

-s, --sleeptime, Timezone for the dates. Defaults: America/Bogota.

-d, --downtime, Amount of seconds to wait to check if the page is up again. Default: 300 (5 min).

-t, --timezone, Amount of minutes to send a summary msg to the channel for how long we have been checking and the page is still down. Default: 360 (6 hours).

## License
Apache License 2.0
