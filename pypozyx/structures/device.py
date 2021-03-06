from pypozyx.structures.byte_structure import ByteStructure
from pypozyx.structures.sensor_data import Coordinates
from pypozyx.structures.generic import Data
from pypozyx.definitions.constants import *


class DeviceCoordinates(ByteStructure):
    byte_size = 15
    data_format = 'HBiii'

    def __init__(self, network_id=0, flag=0, pos=Coordinates()):
        self.network_id = network_id
        self.flag = flag
        self.pos = pos
        self.data = [network_id, flag, pos.x, pos.y, pos.z]

    def load(self, data):
        self.data = data
        self.network_id = data[0]
        self.flag = data[1]
        self.pos = Coordinates(data[2], data[3], data[4])

    def update_data(self):
        try:
            if self.data != [self.network_id, self.flag,
                             self.pos.x, self.pos.y, self.pos.z]:
                self.data = [self.network_id, self.flag,
                             self.pos.x, self.pos.y, self.pos.z]
        except:
            return

    def __str__(self):
        return "ID: 0x{self.network_id:x}, flag: {self.flag}, ".format(self=self) + str(self.pos)


class DeviceRange(ByteStructure):
    byte_size = 10
    data_format = 'IIh'

    def __init__(self, timestamp=0, distance=0, RSS=0):
        self.timestamp = timestamp
        self.distance = distance
        self.RSS = RSS
        self.data = [timestamp, distance, RSS]

    def load(self, data):
        self.data = data
        self.timestamp = data[0]
        self.distance = data[1]
        self.RSS = data[2]

    def update_data(self):
        try:
            if self.data != [self.timestamp, self.distance, self.RSS]:
                self.data = [self.timestamp, self.distance, self.RSS]
        except:
            return

    def __str__(self):
        return '{self.timestamp}ms, {self.distance}mm, {self.RSS}dB'.format(self=self)


class NetworkID(Data):

    def __init__(self, network_id):
        Data.__init__(self, [network_id], 'H')
        self.id = network_id

    def load(self, data):
        self.data = data
        self.id = data[0]

    def update_data(self):
        try:
            if self.data != [self.id]:
                self.data = [self.id]
        except:
            return

    def __str__(self):
        return "0x%0.4x" % self.id


class DeviceList(Data):

    def __init__(self, ids=[], list_size=0):
        if list_size != 0 and ids == []:
            Data.__init__(self, [0] * list_size, 'H' * list_size)
        else:
            Data.__init__(self, ids, 'H' * len(ids))

    def __str__(self):
        s = 'IDs: '
        for i in range(len(self)):
            if i > 0:
                s += ', '
            s += '0x%0.4x' % self[i]
        return s

    def load(self, data):
        for i in range(len(data)):
            self.data[i] = data[i]


# TODO: change UWB settings initialization to not contain data but the parameters.
# data was a lazy step. can always init empty and then load data
# TODO: Think more about UWB settings and whether to make data not like the struct but
# more like the data? Or make this abstraction in the set and get still?
class UWBSettings(ByteStructure):
    byte_size = 7
    data_format = 'BBBBf'

    def __init__(self, channel=0, bitrate=0, prf=0, plen=0, gain_db=0):
        self.channel = channel
        self.bitrate = bitrate
        self.prf = prf
        self.plen = plen
        self.gain_db = gain_db
        self.data = [self.channel, self.bitrate,
                     self.prf, self.plen, self.gain_db]

    def load(self, data):
        self.channel = data[0]
        self.bitrate = data[1] & 0x3F
        self.prf = (data[1] & 0xC0) >> 6
        self.plen = data[2]
        self.gain_db = data[3] / 2
        self.data = [self.channel, self.bitrate,
                     self.prf, self.plen, self.gain_db]

    def update_data(self):
        try:
            if self.data != [self.channel, self.bitrate,
                             self.prf, self.plen, self.gain_db]:
                self.data = [self.channel, self.bitrate,
                             self.prf, self.plen, self.gain_db]
        except:
            return

    def parse_bitrate(self):
        bitrates = {0: '110kbit/s', 1: '850kbit/s', 2: '6.8Mbit/s'}
        try:
            return bitrates[self.bitrate]
        except:
            return 'invalid bitrate'

    def parse_prf(self):
        prfs = {1: '16 MHz', 2: '64 MHz'}
        try:
            return prfs[self.prf]
        except:
            return 'invalid pulse repetitions frequency (PRF)'

    def parse_plen(self):
        plens = {0x0C: '4096 symbols', 0x28: '2048 symbols', 0x18: '1536 symbols', 0x08: '1024 symbols',
                 0x34: '512 symbols', 0x24: '256 symbols', 0x14: '128 symbols', 0x04: '64 symbols'}
        try:
            return plens[self.plen]
        except:
            return 'invalid preamble length'

    def __str__(self):
        return "CH: {}, bitrate: {}, prf: {}, plen: {}, gain: {}dB".format(self.channel, self.parse_bitrate(), self.parse_prf(), self.parse_plen(), self.gain_db)
