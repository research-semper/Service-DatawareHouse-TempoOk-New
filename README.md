# Service-DatawareHouse-TempoOk

## Downloading files from TempoOK

The `main` Lambda accepts an invocation event with the TempoOK file path:

```json
{
  "path": "Comercializadora/Boletins/Diario/2022-03/boletim_TOK_2022-03-31.pdf"
}
```

It posts the path and `TEMPOOK_TOKEN` to the TempoOK download endpoint, then
stores the downloaded file in `s3://semper-datawarehouse/chuva-prevista-smap/`
using the source filename. The Lambda role is restricted to writing under that
prefix.

Set `TEMPOOK_TOKEN` in the deployment environment before deploying. Do not put
the token in source control. The Lambda also requires permission to write to the
configured S3 bucket and prefix.
