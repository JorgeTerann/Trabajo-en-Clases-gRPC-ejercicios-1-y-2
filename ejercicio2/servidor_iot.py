from concurrent import futures
import grpc
import time
from datetime import datetime

import telemetria_pb2
import telemetria_pb2_grpc


class MonitorCadenaFrio(
    telemetria_pb2_grpc.MonitorCadenaFrioServicer
):

    def TransmitirTelemetria(self, request, context):

        if request.id_camion not in ["CAM-001", "CAM-002"]:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                "El camion solicitado no existe"
            )

        if request.intervalo_segundos <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "El intervalo debe ser mayor que cero"
            )

        print("\nCamion conectado:", request.id_camion)

        temperaturas = [5.0, 4.5, 3.8, 1.5, 5.2, 8.5, 6.0, 4.0]

        for temperatura in temperaturas:

            time.sleep(request.intervalo_segundos)

            alerta = temperatura < 2.0 or temperatura > 8.0

            lectura = telemetria_pb2.LecturaSensor(
                id_camion=request.id_camion,
                temperatura_celsius=temperatura,
                latitud=-0.1807,
                longitud=-78.4678,
                timestamp=datetime.now().isoformat(),
                alerta_critica=alerta
            )

            print("Temperatura enviada:", temperatura)
            print("Alerta:", alerta)

            yield lectura


def servir():

    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    telemetria_pb2_grpc.add_MonitorCadenaFrioServicer_to_server(
        MonitorCadenaFrio(),
        servidor
    )

    servidor.add_insecure_port('[::]:50053')

    servidor.start()

    print("Servidor IoT iniciado en puerto 50053")

    servidor.wait_for_termination()


if __name__ == '__main__':
    servir()
