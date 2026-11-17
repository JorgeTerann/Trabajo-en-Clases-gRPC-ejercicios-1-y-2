from concurrent import futures
import grpc

import pagos_pb2
import pagos_pb2_grpc


class ValidadorPagos(pagos_pb2_grpc.ValidadorPagosServicer):

    def VerificarTransaccion(self, request, context):

        print("\nNueva solicitud de pago")
        print("Transacción:", request.id_transaccion)
        print("Monto:", request.monto)

        # Validar monto y tarjeta
        if (request.monto <= 0 or
            len(request.numero_tarjeta) != 16 or
            not request.numero_tarjeta.isdigit()):

            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Monto o número de tarjeta inválido")
            return pagos_pb2.ResultadoPago()

        # Detectar tarjetas bloqueadas
        if request.numero_tarjeta.startswith("4000"):

            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Tarjeta bloqueada por fraude")
            return pagos_pb2.ResultadoPago()

        # Simular país emisor
        emisores = {
            "4111": "US",
            "5200": "MX"
        }

        pais_emisor = emisores.get(request.numero_tarjeta[:4])

        # Verificar pagos mayores a 10000 USD
        if request.codigo_moneda == "USD" and request.monto > 10000:

            if request.pais_origen != pais_emisor:

                return pagos_pb2.ResultadoPago(
                    aprobado=False,
                    codigo_autorizacion="",
                    motivo_rechazo="Rechazado por política de fraude"
                )

        print("Pago aprobado correctamente")

        return pagos_pb2.ResultadoPago(
            aprobado=True,
            codigo_autorizacion="AUTH123456",
            motivo_rechazo=""
        )


def servir():

    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    pagos_pb2_grpc.add_ValidadorPagosServicer_to_server(
        ValidadorPagos(),
        servidor
    )

    servidor.add_insecure_port('[::]:50052')

    servidor.start()

    print("Servidor de pagos iniciado en puerto 50052")

    servidor.wait_for_termination()


if __name__ == '__main__':
    servir()
