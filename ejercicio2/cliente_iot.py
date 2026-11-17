import grpc

import telemetria_pb2
import telemetria_pb2_grpc


def ejecutar():

    with grpc.insecure_channel('localhost:50053') as canal:

        stub = telemetria_pb2_grpc.MonitorCadenaFrioStub(canal)

        peticion = telemetria_pb2.SuscripcionCamion(
            id_camion="CAM-001",
            intervalo_segundos=1
        )

        print("===================================")
        print(" MONITOR DE CADENA DE FRIO IoT")
        print("===================================")

        print("Camion conectado:", peticion.id_camion)

        try:

            for respuesta in stub.TransmitirTelemetria(peticion):

                print("\n------------------------------")

                print("Camion:", respuesta.id_camion)

                print(
                    "Temperatura:",
                    respuesta.temperatura_celsius,
                    "°C"
                )

                print("Latitud:", respuesta.latitud)
                print("Longitud:", respuesta.longitud)
                print("Fecha:", respuesta.timestamp)

                if respuesta.alerta_critica:

                    print("\n¡¡ ALERTA CRITICA DE TEMPERATURA !!")

                else:

                    print("Temperatura normal")

        except grpc.RpcError as e:

            print("\nERROR DE COMUNICACION")
            print("Codigo:", e.code())
            print("Detalle:", e.details())


if __name__ == '__main__':
    ejecutar()
