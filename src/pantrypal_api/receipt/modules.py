from injector import Binder, Module, singleton

from src.core.receipt.accessors.receipt_result_accessor import IReceiptResultAccessor
from src.core.receipt.ports.receipt_gateway_provider import IReceiptGatewayProvider
from src.pantrypal_api.receipt.accessors.receipt_result_accessor import (
    ReceiptResultAccessor,
)
from src.pantrypal_api.receipt.adapters.receipt_gateway_provider import (
    HttpReceiptGatewayProvider,
)


class ReceiptModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            IReceiptGatewayProvider, to=HttpReceiptGatewayProvider, scope=singleton
        )
        binder.bind(IReceiptResultAccessor, to=ReceiptResultAccessor, scope=singleton)
