from ultralytics import YOLO
import cv2
import csv
from datetime import datetime, timedelta

model = YOLO('yolov8n.pt')

def simula_energia(qtd_pessoas, base_energia=100):
    return qtd_pessoas * base_energia

video_path = 'video2.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erro ao abrir o vídeo")
    exit()

start_time = datetime.now()

with open('relatorio_energia.csv', mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    escritor_csv.writerow(['Timestamp', 'Pessoas Detectadas', 'Energia Simulada (W)', 'Observação'])

    frame_num = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    tempo_por_frame = timedelta(seconds=1/fps) if fps > 0 else timedelta(seconds=1/30)  # Fallback

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections = results[0].boxes

        pessoas = [box for box in detections if int(box.cls[0]) == 0]

        num_pessoas = len(pessoas)
        energia = simula_energia(num_pessoas)

        timestamp = start_time + frame_num * tempo_por_frame

        if num_pessoas == 0:
            observacao = "Ambiente vazio"
        elif num_pessoas <= 2:
            observacao = "Poucas pessoas"
        elif num_pessoas <= 5:
            observacao = "Ocupação moderada"
        else:
            observacao = "Alta ocupação"

        # Escreve no CSV
        escritor_csv.writerow([timestamp.strftime('%Y-%m-%d %H:%M:%S'), num_pessoas, energia, observacao])

        # Desenha boxes
        for box in pessoas:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Pessoa", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


        info_text = f"Pessoas: {num_pessoas} | Energia: {energia}W"
        cv2.putText(frame, info_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Detecção de Pessoas e Simulação de Energia", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_num += 1

cap.release()
cv2.destroyAllWindows()
