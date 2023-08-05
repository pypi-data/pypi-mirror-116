ac_table = {
    'commands': [
        '--help',
        '--version',
        '--version-full',
        'hello',
        'executor',
        'pod',
        'flow',
        'ping',
        'gateway',
        'hub',
        'help',
        'pea',
        'client',
        'export-api',
    ],
    'completions': {
        'hello fashion': [
            '--help',
            '--workdir',
            '--download-proxy',
            '--index-data-url',
            '--index-labels-url',
            '--query-data-url',
            '--query-labels-url',
            '--request-size',
            '--num-query',
            '--top-k',
        ],
        'hello chatbot': [
            '--help',
            '--workdir',
            '--download-proxy',
            '--index-data-url',
            '--port-expose',
            '--parallel',
            '--unblock-query-flow',
        ],
        'hello multimodal': [
            '--help',
            '--workdir',
            '--download-proxy',
            '--index-data-url',
            '--port-expose',
            '--unblock-query-flow',
        ],
        'hello fork': ['--help', 'fashion', 'chatbot', 'multimodal'],
        'hello': ['--help', 'fashion', 'chatbot', 'multimodal', 'fork'],
        'executor': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--identity',
            '--workspace-id',
            '--zmq-identity',
            '--port-ctrl',
            '--ctrl-with-ipc',
            '--timeout-ctrl',
            '--ssh-server',
            '--ssh-keyfile',
            '--ssh-password',
            '--uses',
            '--uses-with',
            '--uses-metas',
            '--uses-requests',
            '--py-modules',
            '--port-in',
            '--port-out',
            '--hosts-in-connect',
            '--host-in',
            '--host-out',
            '--socket-in',
            '--socket-out',
            '--memory-hwm',
            '--on-error-strategy',
            '--num-part',
            '--dynamic-routing-out',
            '--dynamic-routing-in',
            '--entrypoint',
            '--docker-kwargs',
            '--pull-latest',
            '--volumes',
            '--gpus',
            '--host',
            '--port-expose',
            '--proxy',
            '--quiet-remote-logs',
            '--upload-files',
            '--disable-remote',
            '--daemon',
            '--runtime-backend',
            '--runtime',
            '--runtime-cls',
            '--timeout-ready',
            '--env',
            '--expose-public',
            '--pea-id',
            '--pea-role',
            '--noblock-on-start',
            '--runs-in-docker',
            '--uses-before',
            '--uses-after',
            '--parallel',
            '--shards',
            '--replicas',
            '--polling',
            '--scheduling',
            '--external',
            '--peas-hosts',
            '--pod-role',
            '--no-dynamic-routing',
            '--connect-to-predecessor',
        ],
        'pod': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--identity',
            '--workspace-id',
            '--zmq-identity',
            '--port-ctrl',
            '--ctrl-with-ipc',
            '--timeout-ctrl',
            '--ssh-server',
            '--ssh-keyfile',
            '--ssh-password',
            '--uses',
            '--uses-with',
            '--uses-metas',
            '--uses-requests',
            '--py-modules',
            '--port-in',
            '--port-out',
            '--hosts-in-connect',
            '--host-in',
            '--host-out',
            '--socket-in',
            '--socket-out',
            '--memory-hwm',
            '--on-error-strategy',
            '--num-part',
            '--dynamic-routing-out',
            '--dynamic-routing-in',
            '--entrypoint',
            '--docker-kwargs',
            '--pull-latest',
            '--volumes',
            '--gpus',
            '--host',
            '--port-expose',
            '--proxy',
            '--quiet-remote-logs',
            '--upload-files',
            '--disable-remote',
            '--daemon',
            '--runtime-backend',
            '--runtime',
            '--runtime-cls',
            '--timeout-ready',
            '--env',
            '--expose-public',
            '--pea-id',
            '--pea-role',
            '--noblock-on-start',
            '--runs-in-docker',
            '--uses-before',
            '--uses-after',
            '--parallel',
            '--shards',
            '--replicas',
            '--polling',
            '--scheduling',
            '--external',
            '--peas-hosts',
            '--pod-role',
            '--no-dynamic-routing',
            '--connect-to-predecessor',
        ],
        'flow': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--workspace-id',
            '--uses',
            '--env',
            '--inspect',
        ],
        'ping': ['--help', '--timeout', '--retries', '--print-response'],
        'gateway': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--identity',
            '--workspace-id',
            '--zmq-identity',
            '--port-ctrl',
            '--ctrl-with-ipc',
            '--timeout-ctrl',
            '--ssh-server',
            '--ssh-keyfile',
            '--ssh-password',
            '--uses',
            '--uses-with',
            '--uses-metas',
            '--uses-requests',
            '--py-modules',
            '--port-in',
            '--port-out',
            '--hosts-in-connect',
            '--host-in',
            '--host-out',
            '--socket-in',
            '--socket-out',
            '--memory-hwm',
            '--on-error-strategy',
            '--num-part',
            '--dynamic-routing-out',
            '--dynamic-routing-in',
            '--prefetch',
            '--prefetch-on-recv',
            '--title',
            '--description',
            '--cors',
            '--default-swagger-ui',
            '--no-debug-endpoints',
            '--no-crud-endpoints',
            '--expose-endpoints',
            '--compress',
            '--compress-min-bytes',
            '--compress-min-ratio',
            '--protocol',
            '--host',
            '--port-expose',
            '--proxy',
            '--daemon',
            '--runtime-backend',
            '--runtime',
            '--runtime-cls',
            '--timeout-ready',
            '--env',
            '--expose-public',
            '--pea-id',
            '--pea-role',
            '--noblock-on-start',
            '--runs-in-docker',
            '--routing-table',
            '--dynamic-routing',
            '--connect-to-predecessor',
        ],
        'hub new': ['--help'],
        'hub push': [
            '--help',
            '--no-usage',
            '--docker-file',
            '--tag',
            '--force',
            '--secret',
            '--public',
            '--private',
        ],
        'hub pull': ['--help', '--no-usage', '--install-requirements'],
        'hub': ['--help', 'new', 'push', 'pull'],
        'help': ['--help'],
        'pea': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--identity',
            '--workspace-id',
            '--zmq-identity',
            '--port-ctrl',
            '--ctrl-with-ipc',
            '--timeout-ctrl',
            '--ssh-server',
            '--ssh-keyfile',
            '--ssh-password',
            '--uses',
            '--uses-with',
            '--uses-metas',
            '--uses-requests',
            '--py-modules',
            '--port-in',
            '--port-out',
            '--hosts-in-connect',
            '--host-in',
            '--host-out',
            '--socket-in',
            '--socket-out',
            '--memory-hwm',
            '--on-error-strategy',
            '--num-part',
            '--dynamic-routing-out',
            '--dynamic-routing-in',
            '--entrypoint',
            '--docker-kwargs',
            '--pull-latest',
            '--volumes',
            '--gpus',
            '--host',
            '--port-expose',
            '--proxy',
            '--quiet-remote-logs',
            '--upload-files',
            '--disable-remote',
            '--daemon',
            '--runtime-backend',
            '--runtime',
            '--runtime-cls',
            '--timeout-ready',
            '--env',
            '--expose-public',
            '--pea-id',
            '--pea-role',
            '--noblock-on-start',
            '--runs-in-docker',
        ],
        'client': [
            '--help',
            '--host',
            '--port-expose',
            '--proxy',
            '--asyncio',
            '--protocol',
        ],
        'export-api': ['--help', '--yaml-path', '--json-path', '--schema-path'],
    },
}
