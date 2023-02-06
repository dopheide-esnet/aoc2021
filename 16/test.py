
import pytest
from aoc16 import Process_Packet

def test1():
    lines = ['8A004A801A8002F478']

    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    Process_Packet(list(input_binary),0,0,versions)
    assert sum(versions) == 16

def test2():
    lines = ['620080001611562C8802118E34']

    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    Process_Packet(list(input_binary),0,0,versions)
    assert sum(versions) == 12

def test3():
    lines = ['C0015000016115A2E0802F182340']

    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    Process_Packet(list(input_binary),0,0,versions)
    assert sum(versions) == 23

def test4():
    lines = ['A0016C880162017C3686B18A3D4780']

    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    Process_Packet(list(input_binary),0,0,versions)
    assert sum(versions) == 31

def test_sum():
    lines = ['C200B40A82']
    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    (idx, values) = Process_Packet(list(input_binary),0,0,versions)
    assert values[0] == 3

def test_prod():
    lines = ['04005AC33890']
    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    (idx, values) = Process_Packet(list(input_binary),0,0,versions)
    assert values[0] == 54

def test_min():
    lines = ['880086C3E88112']
    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    (idx, values) = Process_Packet(list(input_binary),0,0,versions)
    assert values[0] == 7

def test_max():
    lines = ['CE00C43D881120']
    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    (idx, values) = Process_Packet(list(input_binary),0,0,versions)
    assert values[0] == 9

def test_equal():
    lines = ['9C005AC2F8F0']
    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    (idx, values) = Process_Packet(list(input_binary),0,0,versions)
    assert values[0] == 0

def test_final():
    lines = ['9C0141080250320F1802104A08']
    input_bytes = bytes.fromhex(lines[0])
    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)
    versions = []
    (idx, values) = Process_Packet(list(input_binary),0,0,versions)
    assert values[0] == 1