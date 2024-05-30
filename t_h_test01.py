import asyncio
from bleak import BleakClient, BleakScanner

# Definisci gli UUID per il servizio e la caratteristica
char_uuid_notify = "00002b31-0000-1000-8000-00805f9b34fb"
char_uuid_t = "00002a6e-0000-1000-8000-00805f9b34fb"
service_uuid = "0000181a-0000-1000-8000-00805f9b34fb"
nome_device="RAK4630"
async def print_services(client):
    services = await client.get_services()
    print("Discovered Services:")

    for service in services:
        print(f"  UUID: {service.uuid}")
        #if service.name:
        #    print(f"    Name: {service.name}")

        print(f"    Characteristics:")
        for characteristic in service.characteristics:
            print(f"      UUID: {characteristic.uuid}")
            #if characteristic.name:
            #    print(f"        Name: {characteristic.name}")

async def main():
  print("Scanning for Bluetooth devices...")
  devices = await BleakScanner.discover()
  # Attendi il rilevamento di un dispositivo con l'UUID specificato
  for device in devices:
    print(device)
    if device.name == nome_device:
      print(f"Found device: {device.name}")

      # Connettiti al dispositivo
      async with BleakClient(device.address) as client:
        print(f"Connected: {device.name}")
        await print_services(client)
        # Iscriviti alle notifiche per la caratteristica
        await client.start_notify(char_uuid_notify, handle_notification)
        while(True):
            # Aspetta di ricevere una notifica
            print("Waiting for notifications...")
            await asyncio.Event().wait()
            value = await client.read_gatt_char(char_uuid_t)
            # Stampa il valore ricevuto in formato decimale
            print(f"Received value: {value.decode('utf-8')}")
      # Disconnetti dal dispositivo
      print("Disconnected from device")


async def handle_notification(client,client_data):
  # Stampa il valore ricevuto in formato decimale
  print("Received notify")
  print("{0}:{1}".format(client,client_data))


if __name__ == "__main__":
  asyncio.run(main())

