# Automated Dependency Updates for Kubernetes

Categories: `kubernetes`

Renovate supports updating Kubernetes dependencies.

## File Matching

Because file names for kubernetes cannot be easily determined automatically, Renovate will not attempt to match any kubernetes files by default. For details on how to extend a manager's managerFilePatterns value, please follow this link.

## Supported datasources

This manager supports extracting the following datasources: docker, kubernetes-api.

## Default config

```json
{
  "managerFilePatterns": []
}
```

## Additional Information

The kubernetes manager has no managerFilePatterns default patterns, so it won't match any files until you configure it with a pattern. This is because there is no commonly accepted file/directory naming convention for Kubernetes YAML files and we don't want to check every single *.yaml file in repositories just in case any of them have Kubernetes definitions.

If most .yaml files in your repository are Kubernetes ones, then you could add this to your config:

```json
{
  "kubernetes": {
    "managerFilePatterns": ["/\\.yaml$/"]
  }
}
```

If instead you have them all inside a k8s/ directory, you would add this:

```json
{
  "kubernetes": {
    "managerFilePatterns": ["/k8s/.+\\.yaml$/"]
  }
}
```

Or if it's only a single file then something like this:

```json
{
  "kubernetes": {
    "managerFilePatterns": ["/^config/k8s\\.yaml$/"]
  }
}
```

If you need to change the [versioning](https://docs.renovatebot.com/modules/versioning/) format, read the versioning documentation to learn more.

### Open items

The below list of features and bugs were current when this page was generated on January 03, 2026.

Feature requests:
Upper kubernetes limit for kubernetes-api datasource versions [#18696](https://github.com/renovatebot/renovate/issues/18696)

Bug reports:
Line breaks in K8s YAML files lead to missing update detection [#26970](https://github.com/renovatebot/renovate/issues/26970)
