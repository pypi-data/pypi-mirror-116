Anaml Python SDK
================

This repository contains the Anaml Python SDK and some examples that use the
SDK.

Docker Containers
-----------------

The Dockerfile allows you to build two Docker images:

1. An image containing the Anaml Python SDK; and
2. An image containing the Anaml Webhook Server.

```bash
$ docker build --target sdk --tag anaml-sdk .
$ docker build --tag anaml-webhook-server .
```

### Python SDK Image

The Anaml Python SDK image can be used as base image or as a way to access a
Python interpreter with the SDK and all the libraries pre-installed.

```bash
$ docker run --rm -ti anaml-sdk
Python 3.9.6 (default, Jul 22 2021, 15:24:21)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import anaml_client
>>> client = anaml_client.Anaml(url="...", apikey="...", secret="...")
>>>
```

### Webhook Server Image

To deploy the webhook server image you will need to ensure that:

1. The `ANAML_URL`, `ANAML_APIKEY`, and `ANAML_SECRET` environment variables are
   set.

2. Appropriate Google Cloud Platform credentials are exposed in the container in
   such a way that the Data Catalog client library can find them.

Assuming you have the appropriate authentication and environment variables
already set up in your shell, a command similar to this should work for you:  

```bash
$ docker run --rm -ti -p 8080:8080 \
  -e ANAML_URL -e ANAML_SECRET -e ANAML_APIKEY \
  -v ~/.config/gcloud:/root/.config/gcloud \
  anaml-webhook
```

See `examples/webhook-server/README.md` for more details.
