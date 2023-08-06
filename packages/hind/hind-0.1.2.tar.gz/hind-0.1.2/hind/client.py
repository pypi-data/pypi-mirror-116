from boundless import AioHttpClientTransport, Client, cli

from hind.configuration import read_configuration


def get_id_client():
    configuration = read_configuration()

    if (
        "id" not in configuration
        or "scheme" not in configuration["id"]
        or "host" not in configuration["id"]
        or "port" not in configuration["id"]
    ):
        print("Configure hind before use it.")
        exit(1)

    return Client(
        AioHttpClientTransport(
            configuration["id"]["scheme"],
            configuration["id"]["host"],
            configuration["id"]["port"],
        ),
        token=configuration["token"],
    )
