from pcapfile import savefile

nazir_ip = "192.168.0.255"
mix_ip = "127.0.0.1"
num_partners = 1
cap = open('test.pcap', 'rb')
capfile = savefile.load_savefile(cap, layers=2)


def learning(cf):
    non_disjoint_receivers = []
    disjoint_receivers = []
    last_ip_src = ""
    message_sent_from_nazir = False
    current = set()
    for pkt in cf.packets:
        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_dst = pkt.packet.payload.dst.decode('UTF8')
        if message_sent_from_nazir:
            if ip_src == mix_ip and ip_dst not in current:
                current.add(ip_dst)
            elif last_ip_src != ip_src and last_ip_src == mix_ip:
                disjoint = all([current.isdisjoint(s) for s in disjoint_receivers])
                if disjoint:
                    disjoint_receivers.append(current)
                    if len(disjoint_receivers) == num_partners:
                        break
                else:
                    non_disjoint_receivers.append(current)
                message_sent_from_nazir = False
                current = set()
        message_sent_from_nazir = ip_src == nazir_ip or message_sent_from_nazir
        last_ip_src = ip_src
    return non_disjoint_receivers, disjoint_receivers


def excluding(non_disjoint_receivers, disjoint_receivers):
    while not all([(len(disjoint) == 1) for disjoint in disjoint_receivers]):
        for r in non_disjoint_receivers:
            for r_i in disjoint_receivers:
                should_be_added = True
                intersection_r_i = r.intersection(r_i)
                if len(intersection_r_i) == 0:
                    continue
                for r_j in disjoint_receivers:
                    if r_i == r_j:
                        continue
                    intersection_r_j = r.intersection(r_j)
                    if not len(intersection_r_j) == 0:
                        should_be_added = False
                        break
                if should_be_added:
                    disjoint_receivers.remove(r_i)
                    disjoint_receivers.append(intersection_r_i)
    return [e for partners in disjoint_receivers for e in partners]


def sumips(ips):
        print(sum([int(''.join([hex(int(num))[2:].zfill(2) for num in ip.split(".")]), 16) for ip in ips]))


non_disjoint_receivers, disjoint_receivers = learning(capfile)
partners = excluding(non_disjoint_receivers, disjoint_receivers)
sumips(partners)
