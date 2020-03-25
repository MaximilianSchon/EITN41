def diningcryptographers(s_a, s_b, d_a, d_b, m, b):
    a_xor_b = s_a ^ s_b
    broadcastbits = m ^ a_xor_b if (b == 1) else a_xor_b
    message = '{:02x}'.format(d_a ^ d_b ^ broadcastbits)
    broadcast = ('{:02x}'.format(broadcastbits) if (b == 1) else '{:02x}'.format(broadcastbits) + message).upper()
    print(broadcast)

diningcryptographers(int(SA, 16), int(SB, 16), int(DA, 16), int(DB, 16), int(M, 16), b)
