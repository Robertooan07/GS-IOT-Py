from ultralytics import YOLO
import cv2
import csv

# Carrega o modelo YOLOv8 nano
model = YOLO('yolov8n.pt')

# simular energia
def simula_energia(qtd_pessoas, base_energia=100):
    return qtd_pessoas * base_energia


video_path = 'video.mp4' 
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erro ao abrir o vídeo")
    exit()

# arquivo CSV para exportação
with open('saida_dados.csv', mode='w', newline='') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    escritor_csv.writerow(['Frame', 'Qtd_Pessoas', 'Energia_W'])

    frame_num = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

       
        results = model(frame)

       
        detections = results[0].boxes

        
        pessoas = [box for box in detections if int(box.cls[0]) == 0]

        num_pessoas = len(pessoas)
        energia = simula_energia(num_pessoas)

       
        escritor_csv.writerow([frame_num, num_pessoas, energia])

       
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
