# Unraid templates

Community-maintained installation templates by Nishan Goswami.

## Bifrost AI Gateway

This template launches the unmodified official [`maximhq/bifrost:latest`](https://hub.docker.com/r/maximhq/bifrost) image from [Maxim's Bifrost project](https://github.com/maximhq/bifrost).

It follows the upstream Docker deployment:

```sh
docker run -p 8080:8080 -v /path/to/data:/app/data maximhq/bifrost:latest
```

The template supplies only bridge networking, the standard TCP port 8080 and a persistent `/app/data` mount. It contains no application configuration, credentials, providers, models, routes, custom scripts or image modifications. The image's own entrypoint, command and environment defaults are used unchanged.

Install the template, choose an unused host port and appdata directory, then open the WebUI to perform upstream setup. See the [official deployment guide](https://docs.getbifrost.ai/quickstart/gateway/setting-up). Use a fresh appdata directory for a new instance.

This is **Bifrost AI Gateway by Maxim**, not the unrelated Bifrost smart-home hub. The template is community maintained and is not an official Maxim or Unraid listing.

## Support

- [Template issues](https://github.com/nisgoswami/unraid-templates/issues)
- [Upstream application and issues](https://github.com/maximhq/bifrost)
- [Upstream documentation](https://docs.getbifrost.ai)

## License

The template and repository documentation are MIT licensed. The upstream application and its artwork retain their respective upstream licenses and ownership. The application icon is referenced directly from the upstream repository.

## Automatic upstream tracking

GitHub Actions checks the official Docker Hub `maximhq/bifrost:latest` image every six hours and can also be run manually. When its manifest digest changes, the workflow records the digest in `upstream-image.json` and updates the template's changelog. Unchanged images produce no commit. The template continues to use the official `latest` tag; no container is built or repackaged here.

This tracks published images, not individual upstream GitHub commits. The workflow uses GitHub's built-in repository token and anonymous read access to Docker Hub; it needs no personal or server credentials. It does not connect to Unraid or change any running container. Community Apps can ingest the updated template through its normal catalog processing, without a new submission. Actual container installation follows each Unraid server's own update settings.

GitHub schedules are best-effort and may be delayed. GitHub can disable scheduled workflows in public repositories after 60 days without repository activity; re-enable the workflow in Actions if necessary.
