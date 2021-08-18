import math, sys, threading, time, requests, random
from time import sleep
from dataclasses import dataclass

@dataclass
class ConnectivityServiceData:
    start_TS: int = -1
    inter_arrival_time: float = -0.1
    end_TS: int = -1
    type: str = ''
    result: str = ''
    uuid: str = ''
    ber: bool = True

def millis():
    return int(round(time.time() * 1000))

def poisson_wait_time(lmb):
    p = random.random()

    inter_arrival_time = -math.log(1.0 - p) / lmb
    # print('inter_arrival_time: {}'.format(inter_arrival_time))
    return inter_arrival_time

class Connectivity:
    def __init__(self, lmb, connections):
        self.log = []
        self.start_time = -1
        self.end_time = -1
        self.total_holding_time = 0 # no l'entenc. borrar
        
        self.endpoints = {'available': {
            'cs_01': ['tx_node-nep_1', 'rx_node-nep_1'],
            'cs_02': ['tx_node-nep_2', 'rx_node-nep_2'],
            'cs_03': ['tx_node-nep_3', 'rx_node-nep_3'],
            'cs_04': ['tx_node-nep_4', 'rx_node-nep_4']},
            'occupied': {
            }}

        self.max_connections = connections
        self.watcher_thread = threading.Thread(target=self.watcher_function, args=(lmb,))
        self.first_conn = None
        self.n_threads = 0
        self.connection_no_ber = 0
    
    def start(self):
        print('Starting watcher')
        self.watcher_thread.start()
    
    def watcher_function(self, lmb):
        n_connections = 0
        self.start_time = millis()
        while n_connections < self.max_connections:
            s_next = poisson_wait_time(lmb)
            time.sleep(s_next)
            connection = ConnectivityServiceData(inter_arrival_time=s_next)
            next_thread = threading.Thread(target=self.connectivity, args=(connection, ))
            next_thread.start()
            n_connections = n_connections + 1
        self.exit_function()
    
    def connectivity(self, connection):

        connection.type = 'CREATE'
        connection.start_TS = millis()

        self.n_threads = self.n_threads + 1
        try:
            cs_uuid, endpoint = random.choice(list(self.endpoints['available'].items()))
            del self.endpoints['available'][cs_uuid]
            self.endpoints['occupied'][cs_uuid] = endpoint
        except IndexError:
            cs_uuid, endpoint = 'cs_error', ['a', 'b']
            print('No EP available: {}'.format(cs_uuid))

        connection.uuid = cs_uuid
        src = endpoint[0]
        dst = endpoint[1]
        capacity = random.choice([100, 200])

        url = "http://" + ip + "/restconf/config/context/connectivity-service/" + cs_uuid
        # print(url)
        print('SEND cs: {}'.format(cs_uuid))

        response = requests.post(url, json={"uuid": cs_uuid, "src": src, "dst": dst, "capacity": capacity})
        connection.end_TS = millis()

        # print(response.status_code)
        if response.status_code != 201:        # ERROR CASE
            print('Error cs: {} -> {}'.format(cs_uuid, response.json()['description']))
            connection.result = response.json()['description']
            self.log.append(connection)
            del self.endpoints['occupied'][connection.uuid]
            self.endpoints['available'][connection.uuid] = endpoint
            self.n_threads = self.n_threads - 1
            return 0
        else:                                  # SUCCESSFUL CASE
            print('Successful cs: {}'.format(cs_uuid))
            connection.result = response.json()['description']

        self.log.append(connection)
        s_next = poisson_wait_time(mu)
        connection = ConnectivityServiceData()
        connection.inter_arrival_time = s_next
        connection.uuid = cs_uuid
        connection.type = 'DELETE'

        self.delete_cs(connection)

    def delete_cs(self, connection):
        start_ht = millis()
        time.sleep(connection.inter_arrival_time)
        self.total_holding_time = self.total_holding_time + connection.inter_arrival_time
        check_ht = millis() - start_ht
        if check_ht/1000 < 1:
            connection.ber = False

        connection.start_TS = millis()
        try:
            endpoints = self.endpoints['occupied'][connection.uuid]
        except Exception as e:
            print(str(e))
            print(self.endpoints['occupied'])

        url = "http://" + ip + "/restconf/config/context/connectivity-service/" + connection.uuid
        print('SEND delete cs: {}'.format(connection.uuid))
        response = requests.delete(url)
        connection.end_TS = millis()

        if response.status_code != 200:
            print('Error delete cs: {} -> {}'.format(connection.uuid, response.json()['description']))
            connection.result = response.json()['description']
            print(response.content)
        else:
            print('Successful delete cs: {}'.format(connection.uuid))
            connection.result = response.json()['description']
            del self.endpoints['occupied'][connection.uuid]
            self.endpoints['available'][connection.uuid] = endpoints
        self.log.append(connection)
        self.n_threads = self.n_threads - 1

    def exit_function(self):
        print('exit_function')
        self.end_time = millis()
        while self.n_threads != 0:
            sleep(0.5)
        print('Ending test')
        spect_error = 0
        path_error = 0
        created = 0
        deleted = 0
        delete_error = 0
        no_ber = 0
        self.log.sort(key=lambda x: x.start_TS, reverse=False)
        with open('results/log_{}_a{}_h{}_c{}.csv'.format(millis(), lmb_inv, mu_inv, connections), 'w') as filehandle:
            print('WRITING log')
            filehandle.write("Parameters:\n  -N connections: %s\n  -Inter arrival rate: %s(s)\n  -Holding time: %s(s)\n" % (self.max_connections, lmb_inv, mu_inv))
            for connection in self.log:
                if connection.result == 'No spectrum':
                    spect_error = spect_error+1
                elif connection.result == 'No route':
                    path_error = path_error + 1
                elif connection.result == 'OK' and connection.type == 'CREATE':
                    created = created + 1
                elif connection.result == 'OK' and connection.type == 'DELETE':
                    deleted = deleted + 1
                elif connection.result != 'OK' and connection.type == 'DELETE':
                    delete_error = delete_error + 1
                else:
                    print('Should not enter here')
                    print(connection)

                if not connection.ber and connection.type == 'DELETE':
                    no_ber = no_ber + 1

                filehandle.write("%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\n" % (connection.start_TS, connection.inter_arrival_time, connection.end_TS, connection.type, connection.result, connection.ber, connection.uuid))

            filehandle.write("Successfully created: %s\n" % created)
            filehandle.write("Successfully deleted: %s\n" % deleted)

            filehandle.write("Spectrum error: %s\n" % spect_error)
            filehandle.write("Path errors: %s\n" % path_error)
            filehandle.write("Error deleting: %s\n" % delete_error)
            filehandle.write("Error no BER: %s\n" % no_ber)
            assert created+spect_error+path_error == self.max_connections
            filehandle.write("Blocking probability: %s\n" % float((spect_error+path_error)/(created+spect_error+path_error)))
            running_time = float(self.end_time-self.start_time)/1000
            filehandle.write("%s connections in %s seconds\n" % (self.max_connections, running_time))
            cps = self.max_connections/running_time
            filehandle.write("%s connections created per second\n" % (created/running_time))
            filehandle.write("Average interarrival time: %s\n" % cps)
            filehandle.write("Average holding time: %s\n" % (self.total_holding_time/deleted))
            filehandle.write("Erlangs: %s\n" % erlang)


        print('WRITTEN')

# sys.argv[1] = IP@ to send the requests
# sys.argv[2] = Inter arrival time in seconds
# sys.argv[3] = Holding time in seconds
# sys.argv[4] = total number of requests
if __name__ == "__main__":
    ip = sys.argv[1] + ':4900'
    lmb_inv = float(sys.argv[2])
    mu_inv = float(sys.argv[3])
    connections = float(sys.argv[4])

    total_holding_time = 0
    lmb = 1/lmb_inv
    mu = 1/mu_inv
    erlang = lmb*mu_inv
    print('Starting')
    print('\tIp: {}'.format(ip))
    print('\tInter arrival time: {} seconds --> Lambda: {}'.format(lmb_inv, lmb))
    print('\tHolding time: {} seconds --> Mu: {}'.format(mu_inv, mu))
    print('\tErlangs: {}'.format(erlang))
    print('\tTotal connections: {}'.format(connections))
    connectivity = Connectivity(lmb, connections)
    input('Start?')

    connectivity.start()

