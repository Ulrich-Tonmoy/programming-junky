import struct
from pygame.math import Vector2 as vec2
from data_types import *


class WADReader:
    def __init__(self, wad_path):
        self.wad_file = open(wad_path, 'rb')
        self.header = self.read_header()
        self.directory = self.read_directory()

    def read_thing(self, offset):
        read_2_bytes = self.read_2_bytes

        thing = Thing()
        x = read_2_bytes(offset, byte_format='h')
        y = read_2_bytes(offset + 2, byte_format='h')
        thing.angle = read_2_bytes(offset + 4, byte_format='h')
        thing.type = read_2_bytes(offset + 6, byte_format='h')
        thing.flags = read_2_bytes(offset + 8, byte_format='h')
        thing.pos = vec2(x, y)
        return thing

    def read_segment(self, offset):
        read_2_bytes = self.read_2_bytes

        seg = Seg()
        seg.start_vertex_id = read_2_bytes(offset, byte_format='h')
        seg.end_vertex_id = read_2_bytes(offset + 2, byte_format='h')
        seg.angle = read_2_bytes(offset + 4, byte_format='h')
        seg.linedef_id = read_2_bytes(offset + 6, byte_format='h')
        seg.direction = read_2_bytes(offset + 8, byte_format='h')
        seg.offset = read_2_bytes(offset + 10, byte_format='h')
        return seg

    def read_sub_sector(self, offset):
        read_2_bytes = self.read_2_bytes

        sub_sector = SubSector()
        sub_sector.seg_count = read_2_bytes(offset, byte_format='h')
        sub_sector.first_seg_id = read_2_bytes(offset + 2, byte_format='h')
        return sub_sector

    def read_node(self, offset):
        read_2_bytes = self.read_2_bytes
        node = Node()
        node.x_partition = read_2_bytes(offset, byte_format='h')
        node.y_partition = read_2_bytes(offset + 2, byte_format='h')
        node.dx_partition = read_2_bytes(offset + 4, byte_format='h')
        node.dy_partition = read_2_bytes(offset + 6, byte_format='h')

        node.bbox['front'].top = read_2_bytes(offset + 8, byte_format='h')
        node.bbox['front'].bottom = read_2_bytes(offset + 10, byte_format='h')
        node.bbox['front'].left = read_2_bytes(offset + 12, byte_format='h')
        node.bbox['front'].right = read_2_bytes(offset + 14, byte_format='h')

        node.bbox['back'].top = read_2_bytes(offset + 16, byte_format='h')
        node.bbox['back'].bottom = read_2_bytes(offset + 18, byte_format='h')
        node.bbox['back'].left = read_2_bytes(offset + 20, byte_format='h')
        node.bbox['back'].right = read_2_bytes(offset + 22, byte_format='h')

        node.front_child_id = read_2_bytes(offset + 24, byte_format='H')
        node.back_child_id = read_2_bytes(offset + 26, byte_format='H')
        return node

    def read_linedef(self, offset):
        read_2_bytes = self.read_2_bytes
        linedef = LineDef()
        linedef.start_vertex_id = read_2_bytes(offset, byte_format='H')
        linedef.end_vertex_id = read_2_bytes(offset + 2, byte_format='H')
        linedef.flags = read_2_bytes(offset + 4, byte_format='H')
        linedef.line_type = read_2_bytes(offset + 6, byte_format='H')
        linedef.sector_tag = read_2_bytes(offset + 8, byte_format='H')
        linedef.front_sidedef_id = read_2_bytes(offset + 10, byte_format='H')
        linedef.back_sidedef_id = read_2_bytes(offset + 12, byte_format='H')
        return linedef

    def read_vertex(self, offset):
        x = self.read_2_bytes(offset, byte_format='h')
        y = self.read_2_bytes(offset + 2, byte_format='h')
        return vec2(x, y)

    def read_directory(self):
        directory = []
        for i in range(self.header['lump_count']):
            offset = self.header['init_offset'] + i * 16
            lump_info = {
                'lump_offset': self.read_4_bytes(offset),
                'lump_size': self.read_4_bytes(offset + 4),
                'lump_name': self.read_string(offset + 8, num_bytes=8)
            }
            directory.append(lump_info)
        return directory

    def read_header(self):
        return {
            'wad_type': self.read_string(offset=0, num_bytes=4),
            'lump_count': self.read_4_bytes(offset=4),
            'init_offset': self.read_4_bytes(offset=8)
        }

    def read_1_bytes(self, offset, byte_format='B'):
        return self.read_bytes(offset=offset, num_bytes=1, byte_format=byte_format)[0]

    def read_2_bytes(self, offset, byte_format):
        return self.read_bytes(offset=offset, num_bytes=2, byte_format=byte_format)[0]

    def read_4_bytes(self, offset, byte_format='i'):
        return self.read_bytes(offset=offset, num_bytes=4, byte_format=byte_format)[0]

    def read_string(self, offset, num_bytes):
        return ''.join(b.decode('ascii') for b in self.read_bytes(offset, num_bytes, byte_format='c'*num_bytes) if ord(b) != 0).upper()

    def read_bytes(self, offset, num_bytes, byte_format):
        self.wad_file.seek(offset)
        buffer = self.wad_file.read(num_bytes)
        return struct.unpack(byte_format, buffer)

    def close(self):
        self.wad_file.close()
