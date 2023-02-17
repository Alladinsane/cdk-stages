# Stage Configuration
Copy the example or create your own, then generate your project with the --config option*.

```json
[
    {
        "ou-name": {
            "stage-name": [
                "region-code",
                ...
            ],
            ...
        },
        ...
    }
]
```

*If you run cdk-stage without the --config option, the example config will be used to generate sample stages for your project