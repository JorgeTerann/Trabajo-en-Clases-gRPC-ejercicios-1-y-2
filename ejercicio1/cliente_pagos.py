import grpc
import pagos_pb2
import pagos_pb2_grpc


def ejecutar():

    with grpc.insecure_channel('localhost:50052') as canal:

        stub = pagos_pb2_grpc.ValidadorPagosStub(canal)

        pago1 = pagos_pb2.SolicitudPago(
            id_transaccion="TX001",
            numero_tarjeta="4111111111111111",
            monto=150,
            codigo_moneda="USD",
            pais_origen="US"
        )

        pago2 = pagos_pb2.SolicitudPago(
            id_transaccion="TX002",
            numero_tarjeta="4111111111111111",
            monto=-50,
            codigo_moneda="USD",
            pais_origen="US"
        )

        pago3 = pagos_pb2.SolicitudPago(
            id_transaccion="TX003",
            numero_tarjeta="4000123412341234",
            monto=200,
            codigo_moneda="USD",
            pais_origen="US"
        )

        pagos = [pago1, pago2, pago3]

        for pago in pagos:

            print("\n==============================")
            print("Transacción:", pago.id_transaccion)

            try:
                respuesta = stub.VerificarTransaccion(pago)

                if respuesta.aprobado:
                    print("PAGO APROBADO")
                    print("Código:", respuesta.codigo_autorizacion)
                else:
                    print("PAGO RECHAZADO")
                    print("Motivo:", respuesta.motivo_rechazo)

            except grpc.RpcError as e:
                print("ERROR EN LA TRANSACCIÓN")
                print("Código:", e.code())
                print("Detalle:", e.details())


if __name__ == '__main__':
    ejecutar()
