import time
import random
import json
import statistics
from datetime import datetime

class EdgeSensorNode:
    def __init__(self, node_id, threshold=35.0, buffer_size=10):
        self.node_id = node_id
        self.threshold = threshold
        self.buffer_size = buffer_size
        self.data_buffer = []
        
    def get_sensor_reading(self):
        return round(random.uniform(20.0, 45.0), 2)
    
    def process_data_locally(self):
        reading = self.get_sensor_reading()
        self.data_buffer.append(reading)
        
        if len(self.data_buffer) > self.buffer_size:
            self.data_buffer.pop(0)
            
        avg_val = statistics.mean(self.data_buffer)
        
        payload = {

            "timestamp": datetime.now().isoformat(),
            "node_id": self.node_id,
            "current_value": reading,
            "avg_value": round(avg_val, 2)

        }
        
        if reading > self.threshold:
            self.send_to_cloud(payload)
        else:
            print(f"[LOCAL] {self.node_id}: {reading} (Avg: {payload['avg_value']})")
            
    def send_to_cloud(self, payload):
        print("\n" + "!" * 20)
        print("ALERT - THRESHOLD EXCEEDED")
        print(json.dumps(payload, indent=4))
        print("!" * 20 + "\n")
        
def run_system():

    try:
        node_name = input("Enter node ID (e.g. SENSOR_01): ").strip() or "Default_Node"
            
        try:
            limit = float(input("Enter alert threshold: "))
                
        except ValueError:
            print("Invalid input. Using default threshold: 35.0")
            limit = 35.0
                
        node = EdgeSensorNode(node_id=node_name, threshold=limit)
        print(f"System active. Monitoring {node_name}...\n")
        
        while True:
            node.process_data_locally()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nExecution stopped by user. Goodbye!")
            
if __name__ == "__main__":
    run_system()