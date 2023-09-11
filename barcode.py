import cv2
from beep import beep

bd = cv2.barcode.BarcodeDetector()
cap = cv2.VideoCapture(0)

detecciones = {}

while True:
    ret, frame = cap.read()
    if ret:
        (ret_bc, decode, _, puntos) = bd.detectAndDecodeWithType(frame)
        if ret_bc:
            frame = cv2.polylines(frame, puntos.astype(int), True, (0,255,0), 3)
            for codigo, punto  in zip(decode, puntos):
                if codigo in detecciones:
                    detecciones[codigo] += 1
                    if detecciones[codigo] >= 30:
                        print("Detección exitosa", codigo)
                        try:
                            beep()
                        except:
                            print('Beep!!')
                        cv2.waitKey(250)
                        detecciones.clear()
                else:
                    detecciones[codigo] = 1
                frame = cv2.putText(frame, codigo, punto[1].astype(int), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_AA)
        cv2.imshow("Escaner de barras", cv2.resize(frame, (600,400)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
