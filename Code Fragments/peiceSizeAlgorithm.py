'''this is to test verious algorithms for determining the peice size of a torrent'''

def test(torrentSize):
    #piece size = 2^(19+floor(max[Log[2, x] - 28, 0]/2)) # http://www.wolframalpha.com/input/?i=2%5E(19%2Bfloor(max%5BLog%5B2,+x%5D+-+28,+0%5D%2F2)),+x%3D1024*1024*1024*1024%2B1
    #number of peices = ceil(x/2^(19+floor(max[Log[2, x] - 28, 0]/2))) # http://www.wolframalpha.com/input/?i=Plot%5Bceil(x%2F2%5E(19%2Bfloor(max%5BLog%5B2,+x%5D+-+28,+0%5D%2F2))),+%7Bx,+0,+1024*1024*1024*1024%7D%5D
    '''Every time the torrentSize x4, the piece size x2'''
    # min block size 512*1024
    import math
    pieceSize = 2**(19 + math.floor(max(math.log2(torrentSize) - 28, 0) // 2))
    return pieceSize

def test2(torrentSize):
    """Takes a (int)size, returns a (int) peicessize"""
    # http://www.wolframalpha.com/input/?i=Plot%5Bceil(x%2F2%5E(18%2Bfloor(max%5BLog%5B2,+x%5D+-+26,+0%5D%2F2))),+ceil(x%2F2%5E(19%2Bfloor(max%5BLog%5B2,+x%5D+-+28,+0%5D%2F2))),+%7Bx,+0,+1024*1024*1024*1024%7D%5D
    # http://www.wolframalpha.com/input/?i=Plot%5Bceil(x%2F2%5E(18%2Bfloor(max%5BLog%5B2,+x%5D+-+26,+0%5D%2F2))),++x%2F2%5E(18%2B(log_2(x)-26)%2F2),+%7Bx,+0,+1024*1024*1024*1024%7D%5D
    '''Every time the torrentSize x4, the piece size x2'''
    # min block size 256*1024
    import math
    pieceSize = 2**(18 + math.floor(max(math.log2(torrentSize) - 26, 0) // 2))
    return pieceSize

if __name__ == "__main__":
    for i in range(0,64):
        print(i, 2**i, test2(2**i), 2**i//test(2**i), 64*2**i//test(2**i))
