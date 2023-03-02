# Grid is defined as bits, e.g. 0000 0011 0010 0001 = 0 8 4 2 
# i.e. 2 to the power of bits

ROW_MASK = 0xFFFF
COL_MASK = 0x000F_000F_000F_000F

def reverse_row(row):
    return (row >> 12) | ((row >> 4) & 0x00F0)  | ((row << 4) & 0x0F00) | (row << 12)

def transpose(x):
    a1 = x & 0xF0F00F0FF0F00F0F
    a2 = x & 0x0000F0F00000F0F0
    a3 = x & 0x0F0F00000F0F0000
    a = a1 | (a2 << 12) | (a3 >> 12)
    b1 = a & 0xFF00FF0000FF00FF
    b2 = a & 0x00FF00FF00000000
    b3 = a & 0x00000000FF00FF00
    return b1 | (b2 >> 24) | (b3 << 24)

def reverse_row(row):
    return (row >> 12) | ((row >> 4) & 0x00F0)  | ((row << 4) & 0x0F00) | (row << 12) & 0xffff

def unpack_col(row):
    tmp = row
    return (tmp | (tmp << 12) | (tmp << 24) | (tmp << 36)) & COL_MASK

def count_empty(x):
    x |= (x >> 2) & 0x3333333333333333
    x |= (x >> 1)
    x = ~x & 0x1111111111111111
    x += x >> 32
    x += x >> 16
    x += x >>  8
    x += x >>  4
    x & 0xf

# print(bin(combine(0b0011_0001_0001_0001)))
arr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
grid = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_0000

print(hex(reverse_row(0xabcd)))

print(bin(transpose(grid)))



def flatten(bitrow):
    ''' flatten a row of bits to right '''
    # check if bits are all 0000
    x = 0
    pastrow = bitrow
    while x < 3:
        cell = bitrow & (0b1111 << x*4)
        if cell == 0:
            # get first x*4 bits
            firstbits = bitrow & ((2**(x*4))-1)
            # set first x*4 bits to 0
            newrow = bitrow & ~firstbits
            # shift bits to the right
            newrow >>= 4
            # combine with first bits
            bitrow = newrow | firstbits
        if bitrow == pastrow:
            x += 1
        pastrow = bitrow

        # print(bin(bitrow))
    return bitrow

def combine(bitrow):
    ''' combine row of bits to right '''
    bitrow = flatten(bitrow)
    # pairwise comparison
    for x in range(1, 4):
        prev = bitrow & (0b1111 << (x-1)*4) 
        curr = bitrow & (0b1111 << x*4) 
        if prev >> (x-1)*4 == curr >> x*4 and prev != 0:
            bitrow += 0b0001 << (x-1)*4
            # null curr bits
            bitrow &= ~(0b1111 << x*4)

    return flatten(bitrow)

def left(grid):
    ''' move grid left '''
    newgrid = 0
    for x in range(4):
        row = grid & (0b1111_1111_1111_1111 << x*16)
        row >>= x*16
        newrow = combine(row)
        newgrid |= newrow << x*16
    return newgrid

def right(grid):
    ''' move grid right '''
    newgrid = 0
    for x in range(4):
        row = reverse_row(row)
        row = grid & (0b1111_1111_1111_1111 << x*16)
        row >>= x*16
        newrow = combine(row)
        newgrid |= newrow << x*16
    return newgrid

def grid_to_arr(grid, arr):
    ''' convert grid to array '''
    for x in range(4):
        row = grid & (0b1111_1111_1111_1111 << x*16)
        for y in range(4):
            cell = (row & (0b1111 << y*4)) >> y*4
            if cell:
                cell = 2 ** (cell)
            arr[x][y] = cell
    return arr


def reverse_mask(x):
    x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
    x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
    x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
    x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
    x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
    return x


# print(bin(combine(0b0011_0001_0001_0001)))
arr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
grid = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_0000

# print(bin(reverse_mask(0b0011_0001_0001_0001)))

print(bin(transpose(grid)))