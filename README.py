import argparse
import time
from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_bundle_builder import OscBundleBuilder
from pythonosc.osc_bundle import OscBundle

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
                    help="La dirección IP del destino.")
parser.add_argument("--port", type=int, default=7110,
                    help="El puerto del destino.")
args = parser.parse_args()

print(f"Conectando al puerto OSC en {args.ip}:{args.port}...")
client = udp_client.SimpleUDPClient(args.ip, args.port)

connected = False
while not connected:
    try:
        client.send_message("/vrc/client/1/user/message", "Conexión exitosa.")
        connected = True
        print("Conexión exitosa al puerto OSC. Script en línea.")
    except Exception as e:
        print(f"No se pudo conectar al puerto OSC: {e}. Intentando de nuevo...")
        time.sleep(1)

timestamp = time.time()
builder = OscBundleBuilder(timestamp)
for i in range(1, 101):
    msg = OscMessageBuilder("/vrc/client/1/user/message")
    msg.add_arg(str(i))
    builder.add_content(msg.build())
    if i % 10 == 0:
        client.send(builder.build())
        timestamp = time.time()
        builder = OscBundleBuilder(timestamp)
    time.sleep(0.05)

if builder.get_contents():
    bundle = builder.build()
    client.send(bundle)

print("Mensajes enviados con éxito al chat personal de VRchat.")
