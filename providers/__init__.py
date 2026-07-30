from providers.senamhi.collector import SenamhiProvider


PROVIDERS: dict[str, type] = {
    "senamhi": SenamhiProvider,
}
